from tkinter import *
import tkinter.messagebox as tm

class CreateWindow(Frame):
    def __init__(self, master):
        super().__init__(master) #Call the real init

        self.label_nome = Label(self, text="Usuario")
        self.label_senha = Label(self, text="Senha")
        self.label_cpf = Label(self, text="CPF")
        self.label_email = Label(self, text="E-mail")

        self.entry_nome = Entry(self)
        self.entry_senha = Entry(self, show="*") #Show '*' instead of the password
        self.entry_cpf = Entry(self)
        self.entry_email = Entry(self)

        self.label_nome.grid(row=0, sticky=E)
        self.label_senha.grid(row=1, sticky=E)
        self.label_cpf.grid(row=2, sticky=E)
        self.label_email.grid(row=3, sticky=E)
        self.entry_nome.grid(row=0, column=1)
        self.entry_senha.grid(row=1, column=1)
        self.entry_cpf.grid(row=2, column=1)
        self.entry_email.grid(row=3, column=1)

        self.logbtn = Button(self, text="Criar", command=self._new_person())
        self.logbtn.grid(columnspan=1)

        self.pack()

    def _new_person(self):
        pass

class LoginWindow(Frame):
    def __init__(self, master):
        super().__init__(master) #Call the real init

        self.label_username = Label(self, text="Usuario")
        self.label_password = Label(self, text="Senha")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*") #Show '*' instead of the password 

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=1)
        self.logbtn = Button(self, text="Criar", command=self._create_window)
        self.logbtn.grid(columnspan=1)

        self.pack()

    def _create_window(self):
        loop = Tk()
        login = CreateWindow(loop)
        loop.mainloop()

    def _login_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "john" and password == "password":
            tm.showinfo("Info", "Welcome John")
        else:
            tm.showerror("Erro", "Usuario não encontrado")


loop = Tk()
login = LoginWindow(loop)
loop.mainloop()
