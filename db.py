import sqlite3
from sqlite3 import Error

class DataBase:

    def __init__(self):
        pass

    def connect(self):
        try:
            self.data = sqlite3.connect('database/users.db')
        except Error:
            print(Error)
    
    def create_table(self):
        self.curs = self.data.cursor()
        self.curs.execute("CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY, name text, password text, score int, email text)")
        self.data.commit()
    
    def create_user(self, id, name, password, score, email):
        self.curs = self.data.cursor()
        items = (id, name, password, score, email)
        self.curs.execute("INSERT INTO users(id, name, password, score, email) VALUES(?,?,?,?,?)", items)
        self.data.commit()

    def update_score(self, id, new_score):
        self.curs = self.data.cursor()
        self.curs.execute(f"UPDATE users SET score = {new_score} where id = {id}")
        self.data.commit()
    
    def update_password(self, id, new_password):
        self.curs = self.data.cursor()
        self.curs.execute(f"UPDATE users SET password = {new_password} where id = {id}")
    
    def get_ids(self):
        self.curs = self.data.cursor()
        ids = self.curs.execute('SELECT id FROM users').fetchall()
        for id in ids:
            ids[ids.index(id)] = str(id[0])
        return ids
    
    def get_name(self, name):
        self.curs = self.data.cursor()
        names = self.curs.execute('SELECT name FROM users').fetchall()
        print(names)
        for n in names:
            names[names.index(n)] = str(n[0])
        if name in names:
            return True   
        else:
            return False

    def get_pass(self, name, password):
        self.curs = self.data.cursor()
        true_password = self.curs.execute(f'SELECT password FROM users where name="{name}"').fetchall()
        if true_password[0][0] == password:
            return True
        else:
            return False