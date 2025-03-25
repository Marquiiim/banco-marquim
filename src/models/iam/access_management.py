from datetime import datetime
import json
import bcrypt
import re

class User:
    def __init__(self, name, email, password):
        self._name = name
        self._email = email
        self._password_hash = self._hash_password(password)
        self._last_acess = None

    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("[ERROR] Formato de e-mail inválido.")
        self._email = value

    @property
    def password(self):
        raise SystemError("[ERROR] Impossível acessar senha desta forma.")
    
    @password.setter
    def password(self, new_password):
        if len(new_password) < 8:
            raise ValueError("[ERROR] Sua senha deve ter 8 ou mais caracteres.")
        else:
            self._password_hash = self._hash_password(new_password)

    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    def verification_login(self, input_email, input_password) -> bool:
        try:
            data = self.load_data_storage()
            if input_email not in data:
                print("[ERROR] E-mail não registrado.")
                return False
            stored_hash = data[input_email]["Senha"].encode()
            bcrypt.checkpw(input_password.encode(), stored_hash)
        except Exception as e:
            print(f"[ERROR] Falha na verificação: {str(e)}")
            return False


    def verify_password(self, input_password):
        return bcrypt.checkpw(input_password.encode(), self._password_hash)
    
    @property
    def last_acess(self):
        return self._last_acess

    @last_acess.setter
    def last_acess(self, now_acess):
        date_now = datetime.now()
        now_acess = date_now.strftime('%d/%m/%Y - %H:%M:%S')
        self._last_acess = f"{now_acess}"
        
    def data_storage(self, file="../../records/credentials.json"):
        data = {
            self._email: {
                "Nome": self._name,
                "Senha": self._password_hash.decode(),
                "Último acesso": self._last_acess
                }
            }
        
        try:
            with open(file, "r") as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        existing_data.update(data)

        with open(file, "w") as f:
            json.dump(existing_data, f, indent=4)

    def load_data_storage(self, file="../../records/credentials.json"):
        try:
            with open(file, "r") as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}
        return existing_data