# NESTE ARQUIVO ESTÁ A CLASSE COM OS MÉTODOS PARA AS TRANSAÇÕES BANCÁRIAS

from datetime import datetime

class Client:
    def __init__(self, balance=0, withdraw_limit=1000):
        self._balance = balance
        self._withdraw_limit = withdraw_limit
        self.number_transactions = 0
        self.extract = {"Depósitos": [], "Saques": []}

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
        
    def deposit_client(self, value):
        date_now = datetime.now()
        date_str = date_now.strftime('%d/%m/%Y')
        time_str = date_now.strftime('%H:%M:%S')

        if self.number_transactions >= 10:
            print("[ERROR] Você atingiu o número de transações diárias, tente novamente outro dia.")
            return False
        else:
            self.balance += value
            self.number_transactions += 1
            self.extract["Depósitos"].append(f"R${value:.2f} | Dia: {date_str} às {time_str}")
            print(f"Depósito de R${value:.2f} realizado com sucesso.")
            return True
        
    
    def withdraw_client(self, value):
        date_now = datetime.now()
        date_str = date_now.strftime('%d/%m/%Y')
        time_str = date_now.strftime('%H:%M:%S')

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
            self.extract["Saques"].append(f"R${value:.2f} | Dia: {date_str} às {time_str}")
            print(f"Saque de R${value:.2f} realizado com sucesso.")
            return True

    def view_balance(self):
        return f"{self.balance:.2f}"

    def extract_client(self):
        print("========= EXTRATO DE DEPÓSITOS =========")
        print("\n".join(self.extract["Depósitos"]) or "Nenhum depósito realizado.")
        
        print("========= EXTRATO DE SAQUES =========")
        print("\n".join(self.extract["Saques"]) or "Nenhum saque realizado.")