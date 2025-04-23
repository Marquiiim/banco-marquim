from datetime import datetime
from pathlib import Path
import json

class Client:
    _CREDENTIALS_FILE = Path(__file__).parent.parent.parent / "records" / "credentials.json"

    def __init__(self, user=None):
        self._user = user
        self._balance = 0
        self._withdraw_limit = 0
        self.number_transactions = 0
        self.extract = {"Depósitos": [], "Saques": []}

        if user:
            self.load_user()

    # ========= PROPERTIES E SETTERS =========
    @property
    def user(self):
        return self._user
    
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
    def deposit_template(self):
        print(f"""
=========== ÁREA DE DEPÓSITO ===========
        
    SALDO ATUAL: R${self.balance}
              
DIGITE O VALOR DESEJADO PARA DEPOSITAR:       
========================================
""")
        while True:
            try:
                deposit_value = input("Valor: R$")
                value = float(deposit_value)
                return self.deposit_client(value)
            except ValueError:
                print(f"[ERROR] Valor inválido. Use apenas números")


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

    def withdraw_template(self):
        print(f"""
=========== ÁREA DE SAQUE ===========
        
    SALDO ATUAL: R${self.balance}
              
DIGITE O VALOR DESEJADO PARA SACAR:       
=====================================
""")
        while True:
            try:
                withdraw_value = input("Valor: R$")
                value = float(withdraw_value)
                return self.withdraw_client(value)
            except ValueError:
                print(f"[ERROR] Valor inválido. Use apenas números")
        
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
        else:
            self.balance -= value
            self.number_transactions += 1
            self.extract["Saques"].append(f"R${value:.2f} |     {info_transaction}")
            print(f"Saque de R${value:.2f} realizado com sucesso.")
            return True

    # ========= CONSULTAS =========
    def extract_client(self):
        print("========= EXTRATO DE DEPÓSITOS =========")
        print("\n".join(self.extract["Depósitos"]) or "Nenhum depósito realizado.")
        
        print("========= EXTRATO DE SAQUES =========")
        print("\n".join(self.extract["Saques"]) or "Nenhum saque realizado.")

    # ========= MANIPULAÇÃO DE DADOS =========
    def load_user(self):
        try:
            data = self._load_json()

            user_data = data[self.user]
            bank_info = user_data["Informações Bancárias"]

            self._balance = bank_info["Saldo"]
            self._withdraw_limit = bank_info["Limite"]
            self.extract = bank_info["Extrato"]
        except Exception as e:
            print(f"[ERROR] Erro inesperado: {e}")
        
    def _load_json(self, file=_CREDENTIALS_FILE) -> dict[str, any]:
        with open(file, "r", encoding='utf-8') as f:
            return json.load(f)