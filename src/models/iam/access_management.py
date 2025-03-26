from datetime import datetime
import json
import bcrypt
import re

# NESTE ARQUIVO ESTÁ A CLASSE E OS MÉTODOS DE AUTENTICAÇÃO.

class User:
    # ========= CONSTANTES E CONFIGURAÇÕES =========
    _CREDENTIALS_FILE = "../../records/credentials.json"
    _EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
    
    # ========= INICIALIZAÇÃO =========
    def __init__(self, name, email, password):
        self._name = name
        self.email = email  # Usa o setter para validação
        self._password_hash = self._hash_password(password)
        self._last_acess = None

    # ========= PROPRIEDADES E SETTERS =========
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if not re.match(self._EMAIL_REGEX, value):
            raise ValueError("[ERROR] Formato de e-mail inválido.")
        self._email = value

    @property
    def password(self):
        raise SystemError("[ERROR] Impossível acessar senha desta forma.")
    
    @password.setter
    def password(self, new_password):
        if len(new_password) < 8:
            raise ValueError("[ERROR] Sua senha deve ter 8 ou mais caracteres.")
        self._password_hash = self._hash_password(new_password)

    @property
    def last_acess(self):
        return self._last_acess

    @last_acess.setter
    def last_acess(self, value):
        date_now = datetime.now()
        self._last_acess = date_now.strftime('%d/%m/%Y - %H:%M:%S')

    # ========= MÉTODOS DE AUTENTICAÇÃO =========
    def _hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    def verify_password(self, input_password: str) -> bool:
        return bcrypt.checkpw(input_password.encode(), self._password_hash)

    def verify_login(self, input_email: str, input_password: str) -> bool:
        try:
            data = self.load_data_storage()
            if input_email not in data:
                print("[ERROR] E-mail não registrado.")
                return False
            stored_hash = data[input_email]["Senha"].encode()
            return bcrypt.checkpw(input_password.encode(), stored_hash)
        except Exception as e:
            print(f"[ERROR] Falha na verificação: {str(e)}")
            return False

    # ========= MANIPULAÇÃO DE DADOS =========
    def data_storage(self, file: str = None) -> None:
        file = file or self._CREDENTIALS_FILE
        data = {
            self._email: {
                "Nome": self._name,
                "Senha": self._password_hash.decode(),
                "Último acesso": self._last_acess,
                "Informações Bancárias": {
                    "Saldo": 0,
                    "Limite": 1000,
                    "Extrato": {
                        "Depósitos": [],
                        "Saques": []
                    }
                }
            }
        }
        
        existing_data = self._load_json(file)
        existing_data.update(data)

        with open(file, "w") as f:
            json.dump(existing_data, f, indent=4)

    def load_data_storage(self, file: str = _CREDENTIALS_FILE) -> dict:
        return self._load_json(file)

    # ========= MÉTODOS AUXILIARES PRIVADOS =========
    def _load_json(self, file_path: str) -> dict:
            with open(file_path, "r") as f:
                return json.load(f)