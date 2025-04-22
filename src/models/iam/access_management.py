from datetime import datetime
from pathlib import Path
import json, bcrypt, re

from ..banking_options.entities import Client 

# NESTE ARQUIVO ESTÁ A CLASSE E OS MÉTODOS DE AUTENTICAÇÃO.

class User:
    # ========= CONSTANTES E CONFIGURAÇÕES =========
    _CREDENTIALS_FILE = Path(__file__).parent.parent.parent / "records" / "credentials.json"
    _EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
    
    # ========= INICIALIZAÇÃO =========
    def __init__(self, name, email, password):
        self._name = name
        self.email = email
        self._password_hash = self._hash_password(password)
        self._last_acess = None

    # ========= MÉTODOS ESTÁTICOS =========
    @staticmethod
    def login_area():
        print("========= ÁREA DE LOGIN =========")
        email = input("E-mail: ").strip()
        senha = input("Senha: ").strip()
        print("==================================")
        if User.verify_login(input_email=email, input_password=senha):
            return Client(user=email)
    
    @staticmethod
    def register_area():
        print("========= ÁREA DE REGISTRO =========")
        nome = input("Nome: ").strip()
        email = input("E-mail: ").strip()
        senha = input("Senha: ").strip()
        confirm_senha = input("Repita sua senha: ").strip()
        print("==================================")
        if senha != confirm_senha:
            print("[ERROR] Senha não coincidem, tente novamente.")
        else:
            try:
                new_user = User(
                    name = nome,
                    email = email,
                    password = senha
                )
                new_user.last_acess = datetime.now()
                new_user.data_storage()
                print("[SUCESS] Registrado com sucesso!")
                return True
            except ValueError as e:
                print(f"[ERROR]{str(e)}")
                return False
    
    @staticmethod
    def verify_login(input_email, input_password) -> bool:
            data = User.load_data_storage()
            if input_email not in data:
                print("[ERROR] E-mail não registrado.")
                return False
            stored_hash = data[input_email]["Senha"].encode()
            if not bcrypt.checkpw(input_password.encode(), stored_hash):
                print("[ERROR] Senha digitada está errada.")
                return False
            return True
        
    @staticmethod
    def load_data_storage() -> dict:
        try:
            with open(User._CREDENTIALS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    # ========= PROPERTIES E SETTERS =========
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

    # ========= MANIPULAÇÃO DE DADOS =========
    def data_storage(self) -> None:
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
        
        existing_data = User.load_data_storage()        
        existing_data.update(data)

        try:
            with open(self._CREDENTIALS_FILE, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Falha ao salvar dados: {str(e)}")