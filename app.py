from tkinter import *
import tkinter as tk
import tkinter.messagebox as tm
import psycopg2
from database.config import config

GEO = "300x300+120+120"


class LoginWindow(Frame):
    def __init__(self, master):
        super().__init__(master) #Call the real init

        self.title = "GameXP - Competições"

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

        self.pack()

    
    def _info_window(self, person):
        print(person)
        iw = tk.Toplevel()
        iw.geometry(GEO)

        query = "select J.Nick, T.Nome, Po.Posicao from Jogador J join Posicao Po on J.CPF = '{}' join Participa P on J.CPF = '{}' join Time T on P.Tag = T.Tag".format(person[3], person[3])

        row = self.execute_query(query)
        print(row)

        if row is not None:
            self.label_nickname = Label(iw, text="Nickname: '{}'".format(row[0]))
            self.label_team = Label(iw, text="Time partipante: '{}'".format(row[1]))
            self.label_positions = Label(iw, text="Posições em que atua: '{}'".format(row[2]))

            self.label_nickname.grid(row=1, sticky=E)
            self.label_team.grid(row=2, sticky=E)
            self.label_positions.grid(row=3, sticky=E)
            # self.label_championships = Label(self, text="Campeonatos que participa: {}".format())

        

    def _create_window(self):
        create_window = tk.Toplevel()
        create_window.title = "Criar nova conta"
        create_window.geometry(GEO)
        
        create_window.label_nome = Label(create_window, text="Usuario")
        create_window.label_senha = Label(create_window, text="Senha")
        create_window.label_cpf = Label(create_window, text="CPF")
        create_window.label_email = Label(create_window, text="E-mail")

        create_window.entry_nome = Entry(create_window)
        create_window.entry_senha = Entry(create_window, show="*") #Show '*' instead of the password
        create_window.entry_cpf = Entry(create_window)
        create_window.entry_email = Entry(create_window)

        create_window.label_nome.grid(row=0, sticky=E)
        create_window.label_senha.grid(row=1, sticky=E)
        create_window.label_cpf.grid(row=2, sticky=E)
        create_window.label_email.grid(row=3, sticky=E)
        create_window.entry_nome.grid(row=0, column=1)
        create_window.entry_senha.grid(row=1, column=1)
        create_window.entry_cpf.grid(row=2, column=1)
        create_window.entry_email.grid(row=3, column=1)

        create = Button(create_window, text="Criar Login", command=lambda : self._new_person(create_window.entry_nome.get(), create_window.entry_senha.get(),
                                                                                    create_window.entry_cpf.get(), create_window.entry_email.get()))
        create.grid(columnspan=1)
        
        back = Button(create_window, text="Voltar", command=create_window.destroy)
        back.grid(columnspan=2)


    def _login_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        query = "select Nome, Email, Senha, CPF from pessoa where Email = '{}' AND Senha = '{}'".format(username, password)
        row = self.execute_query(query)

        if row is not None:
            name = row[0]
            self._info_window(row)
            tm.showinfo("Info", "Welcome {}".format(name))
        else:
            tm.showerror("Erro", "Usuario não encontrado")
    
    
    def _new_person(self, nome, senha, cpf, email):
        row = self.execute_query("select * from Pessoa where CPF='{}' OR Email='{}'".format(cpf, email))
        if row:
            tm.showerror("Erro", "CPF ou E-mail já existem")
        elif self.insert_table(nome, senha, cpf, email):
            tm.showinfo("Info", "Usuário criado.")
        else:
            tm.showerror("Erro", "Falha na criação de usuário.")


    def insert_table(self, nome, senha, cpf, email):
        """ Connect to the PostgreSQL database server """
        connection = None
        try:
            params = config()
            connection = psycopg2.connect(**params)
            # create a new cursor
            cursor = connection.cursor()         # execute the INSERT statement
            # execute the INSERT statement
            table = "INSERT INTO Pessoa VALUES(%s, %s, %s, %s)"
            table_info = (cpf, email, nome, senha)
            print(table_info)

            cursor.execute(table, table_info)
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
        finally:
            if connection is not None:
                connection.close()


    def execute_query(self, query):
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


loop = Tk()
loop.geometry(GEO)
login = LoginWindow(loop)
loop.mainloop()
