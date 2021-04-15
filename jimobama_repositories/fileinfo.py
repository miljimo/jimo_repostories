import os
import sys
from jimobama_repositories.argsinitialiser import argument_validator


def GetFileInfo(filename):
    info = None
    if(os.path.exists(filename) is True):
        stat_info = os.stat(filename)
        create_t = 0
        modified_t = stat_info.st_mtime
        if(sys.platform == "win32"):
            create_t = stat_info.st_ctime            
        else:
            if(hasattr(stat_info, "st_birthtime")):
                create_t = stat_info.st_birthtime;
            else:
                 create_t  = stat_info.st_ctime;
        info = FileInfo(create_time=create_t, modified_time=modified_t)
    return info


def GetFileCreateTimestamp(filename):
    timestamp = 0
    if(os.path.exists(filename) is True):
        timestamp = GetFileInfo(filename).create_timestamp
    return timestamp


@argument_validator(create_time=0.0000, modified_time=0.0000)
class FileInfo(object):

    def __init__(self, **kwargs):
        self.__CreateTime = kwargs['create_time']
        self.__ModifiedTime = kwargs['modified_time']

    @property
    def create_timestamp(self):
        return self.__CreateTime

    @property
    def modified_timestamp(self):
        return self.__ModifiedTime


if __name__ == "__main__":

    print(GetFileCreateTimestamp("argsinitialiser.py"))
