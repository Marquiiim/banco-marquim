from src.models.iam.access_management import User

while True:
    options = input(f"""
========= ÁREA DE ACESSO =========
    [L] Logar
    [R] Registrar
==================================
""").upper()
    
    if options == "L":
        if User.login_area():
            pass

    elif options == "R":
        if User.register_area():
            pass
        
    else:
        print("[ERROR] Opção inválida, tente novamente.")
