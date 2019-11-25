from tkinter import *
import tkinter.messagebox as tm
import psycopg2
from config import config

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

        botao = Button(self, text="Criar Login", command=lambda : self._new_person())
        botao.grid(columnspan=1)

        self.pack()

    def _new_person(self):
        self.insert_table()

    def insert_table(self):
        """ Connect to the PostgreSQL database server """
        connection = None
        try:
            params = config()
            connection = psycopg2.connect(**params)
            # create a new cursor
            cursor = connection.cursor()
            # execute the INSERT statement
            table = "INSERT INTO Pessoa VALUES(%s, %s, %s, %s)"
            table_info = (str(self.entry_cpf.get()), str(self.entry_email.get()),  str(self.entry_nome.get()), str(self.entry_senha.get()),)
            print(table_info)

            cursor.execute(table, table_info)
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()


def execute_query(query):
    """ query data from the vendors table """
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        cursor.execute(query)
        row = cursor.fetchone()

        if row is not None:
            return row
        
        else:
            return None

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

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

        # # self.logbtn = Button(self, text="Criar nova conta", command=self._create_account())
        # self.logbtn.grid(columnspan=2)

        # # self.logbtn = Button(self, text="Criar nova conta", command=self._create_account())
        # self.logbtn.grid(columnspan=2)

        self.pack()

    def _create_window(self):
        loop = Tk()
        login = CreateWindow(loop)
        loop.mainloop()

    def _login_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        query = "select Nome, Email, Senha from pessoa where Email = '{}' AND Senha = '{}'".format(username, password)
        row = execute_query(query)
        name = row[0]

        if row is not None:
            tm.showinfo("Info", "Welcome {}".format(name))
        else:
            tm.showerror("Erro", "Usuario não encontrado")



loop = Tk()
login = LoginWindow(loop)
loop.mainloop()
