from tkinter import *

def main_window():
	window = Tk()
	window.geometry("400x400")
	window.title("Login")

	Button(text="Login", height="2", width="30").pack() 
	Label(text="").pack()


	username = ''
	
	username_entry = Entry(window, textvariable=username)
	
	window.mainloop()

main_window()
