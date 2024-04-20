'''
    Create a simple sqlite3 database containing two tables, possibleWords and usedWords.
    Upon entering the game, users can choose whether to use all words or only words that haven't been seen yet.
    Users can choose to wipe the database and reset their word history.

    Database schema:
        wordleWords.db
            |
            |--- possibleWords
            |       |--- id : int PRIMARY KEY
            |       |--- word : text NOT NULL
            |       |--- wordLength : int NOT NULL
            |
            |--- usedWords
                    |--- id : int PRIMARY KEY
                    |--- word : text NOT NULL
                    |--- wordLength: int NOT NULL
'''

import pathlib
import sqlite3
from typing import Dict

DB_LOCATION = f'{pathlib.Path(__file__).parent.absolute()}/wordleWords.db'

def create_db(conn:sqlite3.Connection):
    '''
        Create a simple sqlite3 database containing two tables, possibleWords and usedWords.
        Arguments:
            - conn : sqlite3 connection object
    '''
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS possibleWords(
                    id integer PRIMARY KEY,
                    word text NOT NULL,
                    wordLength integer NOT NULL);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS usedWords(
                    id integer PRIMARY KEY,
                    word text NOT NULL,
                    wordLength integer NOT NULL);""")
    conn.commit()
    cursor.close()

def populate_db(conn:sqlite3.Connection):
    '''
        Populate database using words file which is present on most UNIX operating systems.
        Arguments:
            - conn : sqlite3 connection object
    '''
    def read_words_file() -> Dict[int,tuple]:
        '''Read the words file and form necessary info into a dictionary. Returns the dictionary.'''
        with open('/usr/share/dict/words', 'r') as f:
            really_long_file = f.read()
        all_words_ever:Dict[int,tuple] = {}
        count = 0
        for word in really_long_file.split('\n'):
            if len(word) < 3:
                continue
            all_words_ever[count] = (word.upper(), len(word))
            count += 1
        return all_words_ever

    cursor = conn.cursor()
    words = read_words_file()
    for word_id, word_tuple in words.items():
        word, word_length = word_tuple
        data_tuple = (word_id, word, word_length)
        insert_statement = "INSERT INTO possibleWords (id, word, wordLength) VALUES (?, ?, ?);"
        cursor.execute(insert_statement, data_tuple)
        conn.commit()
    cursor.close()

def create_and_populate_db():
    '''Creates and populates wordleWords.db'''
    conn = sqlite3.connect(DB_LOCATION)
    create_db(conn)
    populate_db(conn)
    conn.close()

def main():
    create_and_populate_db()

if __name__ == "__main__":
    main()