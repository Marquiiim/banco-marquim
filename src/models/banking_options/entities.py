from datetime import datetime
import json

class Client:
    _CREDENTIALS_FILE = "../../records/credentials.json"

    def __init__(self, client=None):
        self._client = client
        self._balance = 0
        self._withdraw_limit = 0
        self.number_transactions = 0
        self.extract = {"Depósitos": [], "Saques": []}

        if client:
            self.data_loading()

    # ========= PROPERTIES E SETTERS =========
    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("[ERROR] O valor deve conter apenas números.")
        if value < 0:
            raise ValueError("[ERROR] Valor inválido, tente novamente")
        self._balance = value

    @property
    def withdraw_limit(self):
        return self._withdraw_limit

    # ========= OPERAÇÕES BANCÁRIAS =========
    def deposit_client(self, value):
        date_now = datetime.now()
        info_transaction = date_now.strftime('%d/%m/%Y - %H:%M:%S')

        if self.number_transactions >= 10:
            print("[ERROR] Você atingiu o número de transações diárias, tente novamente outro dia.")
            return False
        
        self.balance += value
        self.number_transactions += 1
        self.extract["Depósitos"].append(f"R${value:.2f} | {info_transaction}")
        print(f"Depósito de R${value:.2f} realizado com sucesso.")
        return True
        
    def withdraw_client(self, value):
        date_now = datetime.now()
        info_transaction = date_now.strftime('%d/%m/%Y - %H:%M:%S')

        if self.number_transactions >= 10:
            print("[ERROR] Você atingiu o número de transações diárias, tente novamente outro dia.")
            return False
        elif value > self.withdraw_limit:
            print(f"[ERROR] Você não pode sacar mais de R${self.withdraw_limit:.2f}.")
            return False
        elif value > self.balance:
            print("[ERROR] Saldo insuficiente para o saque, tente novamente.")
            return False
        
        self.balance -= value
        self.number_transactions += 1
        self.extract["Saques"].append(f"R${value:.2f} | {info_transaction}")
        print(f"Saque de R${value:.2f} realizado com sucesso.")
        return True

    # ========= CONSULTAS =========
    def extract_client(self):
        print("========= EXTRATO DE DEPÓSITOS =========")
        print("\n".join(self.extract["Depósitos"]) or "Nenhum depósito realizado.")
        
        print("========= EXTRATO DE SAQUES =========")
        print("\n".join(self.extract["Saques"]) or "Nenhum saque realizado.")

    # ========= MANIPULAÇÃO DE DADOS =========
    def data_loading(self):
        try:
            data = self._load_json()
            self._client = data["Nome"]
            self._balance = data["Informações Bancárias"]["Saldo"]
            self._withdraw_limit = data["Informações Bancárias"]["Limite"]
            self.extract = data["Informações Bancárias"]["Extrato"]
        except Exception as e:
            print(f"[ERROR] Erro inesperado: {e}")
        
    def _load_json(self, file=_CREDENTIALS_FILE) -> dict[str, any]:
        with open(file, "r", encoding='utf-8') as f:
            return json.load(f)