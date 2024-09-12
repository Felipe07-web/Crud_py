import tkinter as tk
from  tkinter import messagebox


class TelaLogin(tk.Frame):
    def __init__(self, parent):        
        super().__init__(parent) 
        self.parent = parent        
 
 
        self.place(x=0,y=0, width=350,height=200) 
        
        self.label_user = tk.Label(self,text="Usuário:")
        self.label_user.place(x=40,y=20,width=80,height=20)
        
        self.entry_user = tk.Entry(self)
        self.entry_user.place(x=120,y=20,width=200,height=20)
        
        self.entry_user = tk.Entry(self)
        self.entry_user.place(x=120,y=20,width=200,height=20)

        self.label_pwd = tk.Label(self,text="  Senha:")
        self.label_pwd.place(x=40,y=50,width=80,height=20)

        self.entry_pwd = tk.Entry(self, show='*')
        self.entry_pwd.place(x=120,y=50,width=200,height=20)


        self.butt_login = tk.Button(self,text="Login", bg="#87CEEB", font=('Arial', 12, 'bold'), cursor='hand2', command= lambda: self.fazer_login())
        self.butt_login.place(x=50, y=100, width=270, height=30)
        
        
    def fazer_login(self):   

        if (self.entry_user.get() != "") & (self.entry_pwd.get() !=""):     
            self.parent.tela_dash_board()
        else:
            messagebox.showerror("Error","É necessário inserir o usuário e a senha!")
