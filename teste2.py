from tkinter import *
import tkinter.messagebox as tm


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
        self.logbtn.grid(columnspan=2)

        self.pack()

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
