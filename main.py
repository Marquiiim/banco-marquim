from src.models.iam.access_management import User
from src.models.banking_options.entities import Client

while True:
    options = input(f"""
========= ÁREA DE ACESSO =========
    [L] Logar
    [R] Registrar
==================================
""").upper()
    
    if options == "L":
        client = User.login_area() 
        if client:
            while True:
                bank_options = input("""
========= ÁREA DE OPERAÇÕES =========
    [S] Sacar
    [D] Depositar
    [E] Extrato
    [X] Sair
=====================================
""").upper()
                if bank_options == "S":
                    client.withdraw_template()
                elif bank_options == "D":
                    client.deposit_template()
                elif bank_options == "E":
                    client.extract_client()
                else:
                    raise SystemExit

    elif options == "R":
        if User.register_area():
            pass
        
    else:
        print("[ERROR] Opção inválida, tente novamente.")
