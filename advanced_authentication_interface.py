import bcrypt
from tkinter import *
from authentication.connection import select
from authentication.connection import insert


class Application:

    def __init__(self, master=None):
        self.attempts = 0
        self.fonte = ("arial", "12", "bold")
        self.container1 = Frame(master)
        self.container1["pady"] = 30
        self.container1.pack()

        self.container2 = Frame(master)
        self.container2["padx"] = 20
        self.container2["pady"] = 5
        self.container2.pack()

        self.container3 = Frame(master)
        self.container3["padx"] = 20
        self.container3["pady"] = 20
        self.container3.pack()

        self.container4 = Frame(master)
        self.container4["padx"] = 20
        self.container4["pady"] = 20
        self.container4.pack()

        self.container5 = Frame(master)
        self.container4["padx"] = 20
        self.container4["pady"] = 20
        self.container5.pack()

        self.title = Label(self.container1, text="Informe os dados :")
        self.title["font"] = ("Arial", "12", "bold")
        self.title.pack()

        self.lblName = Label(self.container2, text="User:", font=self.fonte, width=10)
        self.lblName.pack(side=LEFT)

        self.txtName = Entry(self.container2)
        self.txtName["width"] = 25
        self.txtName["font"] = self.fonte
        self.txtName.pack(side=LEFT)

        self.lblPassword = Label(self.container3, text="Password:", font=self.fonte, width=10)
        self.lblPassword.pack(side=LEFT)

        self.txtPassword = Entry(self.container3)
        self.txtPassword["width"] = 25
        self.txtPassword["show"] = "*"
        self.txtPassword["font"] = self.fonte
        self.txtPassword.pack(side=LEFT)

        self.btnLogin = Button(self.container4, text="Login", font=self.fonte, bg="green", width=6)
        self.btnLogin["command"] = self.login
        self.btnLogin.pack(side=LEFT)

        self.btnCreate = Button(self.container4, text="Create", font=self.fonte, bg="orange", width=6)
        self.btnCreate["command"] = self.create
        self.btnCreate.pack(side=LEFT)

        self.btnExit = Button(self.container4, text="Exit", font=self.fonte, bg="red", width=6)
        self.btnExit["command"] = self.exit
        self.btnExit.pack(side=RIGHT)

        self.lblMessage = Label(self.container5, text="")
        self.lblMessage["font"] = ("Arial", "12", "italic")
        self.lblMessage.pack()

    def login(self):
        if self.attempts < 5:
            varName = ("'" + self.txtName.get() + "'")
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

                if bcrypt.checkpw(str.encode(self.txtPassword.get(), "utf-8"), password_hashed):
                    self.attempts = 0
                    self.lblMessage["text"] = "Usuario autenticado com sucesso!"
                    self.txtPassword.delete(0, END)
                else:
                    self.attempts = self.attempts + 1
                    self.lblMessage["text"] = "Usuario ou senha incorretos!"
                    self.txtPassword.delete(0, END)
            else:
                self.lblMessage["text"] = "Usuario ou senha incorretos!"
                self.txtPassword.delete(0, END)
        else:
            self.lblMessage["text"] = "Tentativas de login excedidas, usuario bloqueado!"
            self.txtPassword.delete(0, END)

    def create(self):
        varNewName = ("'" + self.txtName.get() + "'")
        query_verify_user = select("usuario_nome", "usuario", "usuario_nome = " + varNewName)

        if query_verify_user:
            self.lblMessage["text"] = "Usuario já existe, escolha um novo usuario!"
            self.txtPassword.delete(0, END)

        else:
            hashed = bcrypt.hashpw(str.encode(self.txtPassword.get(), "utf-8"), bcrypt.gensalt())

            str_hashed = str(hashed)
            bd_hashed = str_hashed.replace("'", "")
            varNewPassword = ("'" + bd_hashed + "'")

            values = ["DEFAULT, " + varNewName + ", " + varNewPassword]
            insert(values, "usuario")

            self.lblMessage["text"] = "Usuario criado com sucesso, realize o login."
            self.txtPassword.delete(0, END)

    def exit(self):
        # root.messagebox.showinfo("Usuario autenticado com sucesso!")
        self.lblMessage["text"] = "Programa finalizado!"
        sys.exit(0)


root = Tk()
root.title("Interface of Authentication")
Application(root)
root.mainloop()
