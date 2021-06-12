from cryptography.fernet import Fernet
from injector import inject
from infrastructor.dependency.scopes import IScoped
from models.configs.ApiConfig import ApiConfig


class CryptoService(IScoped):
    @inject
    def __init__(self, api_config: ApiConfig):
        self.api_config = api_config

    def decrypt_code(self, crypted_text):
        secret_key = self.api_config.secret_key.encode()
        f = Fernet(secret_key)
        return f.decrypt(crypted_text)

    def encrypt_code(self, decrypted_text):
        secret_key = self.api_config.secret_key.encode()
        f = Fernet(secret_key)
        return f.encrypt(decrypted_text)
