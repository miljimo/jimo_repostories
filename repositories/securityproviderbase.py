class SecurityProviderBase(object):

    def __init__(self):
        self.dont_secure  =  True;
        pass;

    def encrypt(self, plain_text:str):
        pass;
    def decrypt(self, cipher_text:str):
        pass;
    