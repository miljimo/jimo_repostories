import os
import sys
import json
import uuid
import hashlib
import warnings
import base64
from datetime import datetime
import threading
from jimo_repositories.fileinfo import *
import jimo_repositories.argsinitialiser as argsint


CREATE_DATE_TIME_FIELD = "CreateDateTime"
REPOSITORY_HASH_KEY = "Hash"


"""
File mode creations
"""


class OpenMode(int):
    """
     Create a new file for read, if the 
    """
    CREATE_EXIST_OPEN_WRITE = 0b0001
    CREATE_EXIST_OPEN_READ = 0b0010
    CREATE_NEW = 0b0100
    ALL = CREATE_EXIST_OPEN_WRITE | CREATE_EXIST_OPEN_READ | CREATE_NEW


"""
 Create group of repository that you can commit at the same time.
"""


class RepositoryGroup(object):
    def __init__(self, owner):
        self.__repos = dict()
        self.__owner = owner
        self.__synclocker = threading.Lock()

    def create(self, filename):
        FPSTimer.FPSLocker(self.__synclocker)
        if(filename in self.__repos) is not True:
            repo = Repository(filename)
            self.__repos[filename] = repo
            return repo
        return self.__repos[filename]

    def remove(self, filename: str):
        if(filename in self.__repos):
            del self.__repos[filename]

    def commit(self):
        FPSTimer.FPSLocker(self.__synclocker)
        for key in self.__repos:
            repo = self.__repos[key]
            repo.commit()
        self.__owner.commit()


@argsint.argument_validator(data=None,
                            open_mode=OpenMode.ALL)
class Repository(object):
    __HASH_KEY__ = "hash_key"

    def __init__(self, filename: str, **kwargs):
        self.__data = kwargs["data"]
        self.__open_mode = kwargs["open_mode"]
        self.__filename = filename
        self.can_read = False
        self.can_write = False
        self._DesignChanges = False

        if(self.__data is None):
            # we dont need to load from the database file.
            self.__data = self.__open_data_file(filename, self.__open_mode)
        self.content_tempered = self.has_changed or self._DesignChanges
        self.is_open = self.data is not None
        self.__folder = os.path.dirname(filename)
        self.__groups = None

    def create_group(self):
        if(self.__groups is None):
            self.__groups = RepositoryGroup(self)
        return self.__groups

    def __open_data_file(self, filename: str, open_mode: int):
        self.content_tempered = False
        data = None
        if(os.path.exists(filename) is not True):
            if (((open_mode >> (OpenMode.CREATE_NEW >> 1)) & 0x01) == 0x01):
                self.__create_directory_and_files(filename)
        data = self.__load_database(filename)
        if(data is None):
            raise IOError("Unable to load database {0}".format(filename))
        # if its read only then we shall preverted the user to write.
        if(((open_mode >> (OpenMode.CREATE_EXIST_OPEN_READ >> 1)) & 0x01) == 0x01):
            self.can_read = True
        # Do for write only.
        if(((open_mode >> (OpenMode.CREATE_EXIST_OPEN_WRITE >> 1)) & 0x01) == 0x01):
            self.can_write = True
        if(CREATE_DATE_TIME_FIELD in data) is not True:
            data[CREATE_DATE_TIME_FIELD] = GetFileCreateTimestamp(
                self.filename)

        if(self.__HASH_KEY__ in data):
            data[REPOSITORY_HASH_KEY] = data[self.__HASH_KEY__]
            del data[self.__HASH_KEY__]
            self._DesignChanges = True
        return data

    @property
    def has_changed(self):
        current_hash = self.get(REPOSITORY_HASH_KEY, "#")
        self.remove(REPOSITORY_HASH_KEY)
        content = json.dumps(self.data).encode("utf-8")
        haschanged = (self.create_hash(content) != current_hash)
        self.add(REPOSITORY_HASH_KEY, current_hash)
        return haschanged

    @has_changed.setter
    def has_changed(self, status: bool):
        warnings.warn("has_changed property has now be depreciated.")
        pass

    @property
    def filename(self):
        return self.__filename

    @property
    def folder(self):
        return self.__folder

    @property
    def data(self):
        return self.__data

    def create_new_content_hash(self):
        prev_hash = self.get("Hash")
        self.remove(REPOSITORY_HASH_KEY)
        content = json.dumps(self.data).encode("utf-8")
        self.add(REPOSITORY_HASH_KEY, prev_hash)
        return self.create_hash(content)

    def create_hash(self, content: bytes):
        sha256 = hashlib.sha256()
        sha256.update(content)
        return sha256.hexdigest()

    def add(self, name, value):
        status = False
        if(type(name) == str):
            if(name.strip() != ""):
                if(self.__acceptable_type(value) is not True):
                    raise ValueError("@Unknown type = {0}".format(type(value)))
                if(self.data is not None):
                    if(name in self.data):
                        if(self.data[name] != value):
                            self.data[name] = value
                    else:
                        self.data[name] = value
                    status = True
        return status

    def create(self, name, default: None):
        if(type(name) != str):
            raise TypeError("@name : expecting it to be a string type")
        result = default
        if(name in self.data) is not True:
            self.add(name, result)
        return self.data[name]

    def remove(self, name):
        status = False
        if(self.data is not None):
            if(name in self.data):
                del self.data[name]
                status = True
        return status

    def get(self, name, default: object = None):
        result = default
        if(self.data != None):
            if(name in self.data):
                result = self.data[name]
        return result

    def commit(self, **kwargs):
        status = False
        if(type(self.data) == dict):
            if(self.has_changed is True) or (self.content_tempered is True):
                # Dont hash the key with the content.
                self.remove
                self.remove(REPOSITORY_HASH_KEY)
                # content without hash-key
                contents_without_key = json.dumps(self.data).encode("utf-8")
                # add the key
                self.__data[REPOSITORY_HASH_KEY] = self.create_hash(
                    contents_without_key)
                contents_with_key = json.dumps(self.data).encode("utf-8")
                with open(self.filename, mode="wb+") as file:
                    file.write(contents_with_key)
                self.content_tempered = False
        return status

    def has(self, value: object, valuelists: list):
        status = False
        if(type(valuelists) == list):
            for val in valuelists:
                if(val == value):
                    status = True
                    break
        return status

    def contains(self, key: str):
        status = False
        if(key in self.data):
            status = True
        return status

    def __acceptable_type(self, value):
        status = False
        if(type(value) == dict) \
                or (type(value) == list) \
                or (type(value) == int)\
                or (type(value) == float) \
                or (type(value) == bool) \
                or (type(value) == str):
            status = True
        return status

    def __load_database(self, filename: str):
        database = None
        if(os.path.exists(filename)):
            with open(filename, mode='rb+') as file:
                obj = None
                try:
                    content = file.read()
                    if(content):
                        obj = json.loads(content)
                    else:
                        obj = dict()
                except Exception as err:
                    obj = dict()
                if(type(obj) != dict):
                    raise ValueError(
                        "@expecting a database content to be a dictionary")
                database = obj
        return database

    def __create_directory_and_files(self, path: str):
        if(os.path.exists(path) is not True):
            directoryRoot = os.path.dirname(os.path.abspath(path))

            if(os.path.exists(directoryRoot) is not True):
                os.makedirs(directoryRoot, exist_ok=True)
            self.__create_if_not_exists(path)

    def __create_if_not_exists(self, filename: str):
        status = False
        if(type(filename) == str) and (os.path.exists(filename) is not True):
            with open(filename, mode='w+') as file:
                status = True
        return status


"""
 This will managed all the repo on the system.
"""


class Management(object):

    def __init__(self):
        self.__repositories = dict()

    def create(self, filename: str, **kwargs) -> Repository:
        if(type(filename) == str):
            if(filename in self.__repositories) is not True:
                self.__repositories[filename] = self._create_instance(
                    filename, **kwargs)
        return self.get(filename)

    def remove(self, filename):

        if(filename in self.__repositories):
            del self.__repositories[filename]
            return True
        return False

    def get(self, filename: str) -> Repository:
        repo = None
        if(filename in self.__repositories):
            repo = self.__repositories[filename]
        else:
            if(os.path.exists(filename)):
                repo = self._create_instance(filename)
        return repo

    def _create_instance(self, filename: str, **kwargs) -> Repository:

        repo = None
        if(filename in self.__repositories) is not True:
            repo = Repository(filename)
        return repo

    def commit(self):

        for path in self.__repositories:
            if(path is not None):
                repo = self.__repositories[path]
                if(repo is not None):
                    repo.commit()


# Create a repository managed object.
mgr = Management()


def get_repository(filename: str) -> Repository:
    global mgr
    return mgr.get(filename)


def get_manager():
    global mgr
    return mgr


def create_if_not_exists_repository(filename: str) -> Repository:
    global mgr
    return mgr.create(filename)


def commit_all():
    global mgr
    if(mgr is not None):
        mgr.commit()


if __name__ == "__main__":
    repo = create_if_not_exists_repository("./data/database.json");
    res = Repository("./data/database.json")
    if(isinstance(res, Repository)):
        print("Valid instance")

    print(len(res.data))
