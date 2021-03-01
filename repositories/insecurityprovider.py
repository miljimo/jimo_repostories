import base64;
from  repositories.securityproviderbase import SecurityProviderBase

class InSecurityProvider(SecurityProviderBase):
    def __init__(self):
        super().__init__();
        pass;

    def encrypt(self, plaintext:bytes):
        if(self.dont_secure is True):
            return plaintext;
        return base64.encodebytes(plaintext)
        
    def decrypt(self, cipher:bytes):
        if(self.dont_secure is True):
            return cipher;
        return base64.decodebytes(cipher);