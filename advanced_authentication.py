import sys
import bcrypt
from authentication.connection import select
from authentication.connection import insert

attempts = 0

while True:
    op = int(input("Digite a opção: 1- Fazer login 2- Criar novo usuario 3- Fechar programa"))

    if op == 1:
        if attempts < 5:
            name = input("Digite seu nome de usuario: ")
            password = input("Digite sua senha: ")

            varName = ("'" + name + "'")
            query_select_name = select("usuario_nome", "usuario", "usuario_nome = " + varName)

            if query_select_name:
                query_select_password = select("usuario_senha", "usuario", "usuario_nome = " + varName)

                password_hashed = str(query_select_password[0])
                password_hashed = password_hashed.replace("'usuario_senha':", "")
                password_hashed = password_hashed.replace("{", "")
                password_hashed = password_hashed.replace("}", "")
                password_hashed = password_hashed.replace(" ", "")
                password_hashed = password_hashed.replace("'", "")
                password_hashed = password_hashed.replace("b", "", 1)
                password_hashed = bytes(password_hashed, "utf-8")

                if bcrypt.checkpw(str.encode(password, "utf-8"), password_hashed):
                    attempts = 0
                    print("Usuario autenticado com sucesso!")
                else:
                    attempts = attempts + 1
                    print("Usuario ou senha incorretos!")
            else:
                print("Usuario ou senha incorretos!")
        else:
            print("Tentativas de login excedidas, usuario bloqueado!")

    elif op == 2:
        newName = input("Digite um nome de usuario: ")
        varNewName = ("'" + newName + "'")

        query_verify_user = select("usuario_nome", "usuario", "usuario_nome = " + varNewName)

        if query_verify_user:
            print("Usuario já existe, escolha um novo usuario!")

        else:
            newPassword = input("Digite uma senha: ")
            hashed = bcrypt.hashpw(str.encode(newPassword, "utf-8"), bcrypt.gensalt())

            str_hashed = str(hashed)
            bd_hashed = str_hashed.replace("'", "")
            varNewPassword = ("'" + bd_hashed + "'")

            values = ["DEFAULT, " + varNewName + ", " + varNewPassword]
            query = insert(values, "usuario")

            print("Usuario criado com sucesso, realize o login.")

    elif op == 3:
        print("Programa finalizado!")
        sys.exit(0)

    else:
        print("Escolha uma option valida!")
