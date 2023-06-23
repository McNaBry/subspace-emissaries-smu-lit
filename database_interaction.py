# reference for db schema
# cursor.execute(
import sqlite3
import bcrypt
from datetime import datetime

def see_all(table):
    """for testing only"""
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM {table}"
        rows = cursor.execute(query).fetchall()
        return rows

def delete_all(table):
    """for testing only"""
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = f"DELETE FROM {table}"
        cursor.execute(query).fetchall()

def create_lawyer_table():
    """Creating SQL table for lawyers"""
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = """
        CREATE TABLE lawyers (
	    name TEXT PRIMARY KEY,
            law_firm TEXT NOT NULL,
            experience INTEGER NOT NULL,
            tag TEXT NOT NULL,
            language_proficiency TEXT NOT NULL
        );
        """
        cursor.executescript(query)

def query_lawyers(tag:str, language:str):
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = f"SELECT name, law_firm, experience FROM lawyers WHERE language_proficiency Like '%{language}%' AND tag Like '%{tag}%'"
        rows = cursor.execute(query).fetchall()
        return rows

def check_existing_lawyer(name:str):
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM lawyers WHERE name Like '{name}'"
        rows = cursor.execute(query).fetchall()
        return rows != []

def add_lawyers(lawyer_list:str):
    """format: name1,firm1,exp1,tag1,lp1\n\rname2,firm2,exp2,tag2,lp2"""
    list = lawyer_list.split("\n\r")
    for lawyer in list:
        lawyer = lawyer.split(",")
        name = lawyer[0]
        law_firm = lawyer[1]
        experience = lawyer[2]
        tag = lawyer[3]
        language_proficiency = lawyer[4]
        with sqlite3.connect("kirby.sqlite") as connection:
            cursor = connection.cursor()
            query = f"INSERT INTO lawyers (name, law_firm, experience, tag, language_proficiency) VALUES ('{name}', '{law_firm}', '{experience}', '{tag}', '{language_proficiency}')"
            cursor.execute(query)
            connection.commit()

def create_user_table():
    """Creating SQL table for users"""
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = """
        CREATE TABLE users (
            email TEXT NOT NULL,
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );
        """
        cursor.executescript(query)

def check_existing_user(username:str):
    """Checking if username already exists in database"""
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM users WHERE username Like '{username}'"
        rows = cursor.execute(query).fetchall()
        return rows != []

def add_user(email:str, username:str, password:str):
    """Inserting new user into database"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt).hex()
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = f"INSERT INTO users(email, username, password) VALUES ('{email}','{username}','{hash}')"
        cursor.execute(query)
        connection.commit()

def user_log_in(username:str, password:str):
    """Verifying user's password when attempting to log in"""
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = f"SELECT password FROM users WHERE username Like '{username}'"
        row = cursor.execute(query).fetchall()
        hash = bytes.fromhex(row[0][0])

        userBytes = password.encode('utf-8')
        return bcrypt.checkpw(userBytes, hash)

def create_history_table():
    """creating table to store user chat history"""
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = """
        CREATE TABLE history (
        username TEXT NOT NULL,
        date TEXT NOT NULL,
        conversation TEXT NOT NULL,
        PRIMARY KEY(username, date)
        );
        """
        cursor.executescript(query)

def save_user_convo(username:str, conversation:str):
    """storing past user's past conversation with K.I.R.B.Y. into the database"""
    now = f"{datetime.now():%d-%m-%Y}"
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM history WHERE username Like '{username}' AND date Like '{now}'"
        row = cursor.execute(query).fetchall()
        if row:
            temp = row[0][-1]
            conversation += "||" + temp
            print("SAVE",conversation)
            query = f"UPDATE history SET conversation = '{conversation}' WHERE username = '{username}' AND date = '{now}'"
        else:
            print("SAVE",conversation)
            query = f"INSERT INTO history (username, date, conversation) VALUES ('{username}', '{now}', '{conversation}')"
        cursor.execute(query)
        connection.commit()

def get_all_user_convo(username:str):
    """retrieving user past conversations"""
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM history WHERE username Like '{username}'"
        rows = cursor.execute(query).fetchall()
        return rows

def get_user_convo(username:str, date:str):
    """retrieving user past conversations"""
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM history WHERE username Like '{username}' and date Like '{date}'"
        rows = cursor.execute(query).fetchall()
        return rows

def get_user_use_dates(username:str):
    """retrieving user past conversations"""
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = f"SELECT date FROM history WHERE username Like '{username}'"
        rows = cursor.execute(query).fetchall()
        return rows

def remove_user_convo(username:str, date:str):
    """removing a conversation from user's history"""
    with sqlite3.connect("kirby.sqlite") as connection:
        cursor = connection.cursor()
        query = f"DELETE FROM history WHERE date Like '{date}' AND username Like '{username}'"
        cursor.execute(query)
