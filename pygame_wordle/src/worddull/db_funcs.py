import pathlib
import sqlite3
from random import randint
from typing import Tuple, List
from timing.timers import time_it

DB_LOCATION = f'{pathlib.Path(__file__).parent.absolute()}/worddullWords.db'

def move_word_to_table(word_info:Tuple[int, str, int], new_table:str) -> None:
    '''
        Copy word entry into a new table, then remove it from the original table.
        Arguments:
            - word_info : tuple containing (word_id, word, word_length)
            - new_table (table you want to move to) : 'possibleWords' or 'usedWords'
    '''

    def delete_word_from_table(conn:sqlite3.Connection, word_info:Tuple[int, str, int], old_table:str) -> None:
        '''
            Delete word entry from table.
            Arguments:
                - conn : sqlite3 connection object
                - word_info : tuple containing (word_id, word, word_length)
                - old_table (table you want to delete from) : 'possibleWords' or 'usedWords'
        '''
        word_id = word_info[0]
        cursor = conn.cursor()
        if old_table == 'possibleWords':
            sql_statement = 'DELETE FROM possibleWords WHERE id = ?;'
        elif old_table == 'usedWords':
            sql_statement = 'DELETE FROM usedWords WHERE id = ?;'
        else:
            print('Something went wrong with arguments to DB')
            cursor.close()
            conn.close()
            quit()
        cursor.execute(sql_statement, (word_id,))
        conn.commit()
        cursor.close()

    conn = sqlite3.connect(DB_LOCATION)
    cursor = conn.cursor()
    if new_table == 'possibleWords':
        old_table = 'usedWords'
        sql_statement = 'INSERT INTO possibleWords (id, word, wordLength) VALUES (?, ?, ?);'
    elif new_table == 'usedWords':
        old_table = 'possibleWords'
        sql_statement = 'INSERT INTO usedWords (id, word, wordLength) VALUES (?, ?, ?);'
    else:
        print('Something went wrong with arguments to DB')
        cursor.close()
        conn.close()
        quit()
    cursor.execute(sql_statement, word_info)
    conn.commit()
    cursor.close()
    delete_word_from_table(conn, word_info, old_table)
    conn.close()

def select_random_word(table:str, word_length:int) -> Tuple[int, str, int]:
    '''
        Query a table for all words of a specified length, then generate a random index and returns a couple containg the (word_id, word, and word_length).
        Arguments:
            - table (table you want to query) : 'possibleWords' or 'usedWords'
            - word_length : integer, must be a valid length, but will be provided by selecting a button on the main menu
    '''
    conn = sqlite3.connect(DB_LOCATION)
    cursor = conn.cursor()
    if table == 'possibleWords':
        sql_statement = 'SELECT * FROM possibleWords WHERE wordLength = ?;'
    elif table == 'usedWords':
        sql_statement = 'SELECT * FROM usedWords WHERE wordLength = ?;'
    else:
        print('Something went wrong with arguments to DB')
        cursor.close()
        conn.close()
        quit()
    cursor.execute(sql_statement, (word_length,))
    all_rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(all_rows) == 1:
        return all_rows[0]
    elif len(all_rows) == 0:
        return False
    random_word_index = randint(0, len(all_rows)-1)
    return all_rows[random_word_index]

def select_all_word_lengths(table:str) -> List[int]:
    '''
        Query a table for distinct values in the wordLength column. returns a list of valid word lengths in the table.
        Arguments:
            - table (table you want to query) : 'possibleWords' or 'usedWords'
    '''
    conn = sqlite3.connect(DB_LOCATION)
    cursor = conn.cursor()
    if table == 'possibleWords':
        sql_statement = 'SELECT DISTINCT wordLength FROM possibleWords;'
    elif table == 'usedWords':
        sql_statement = 'SELECT DISTINCT wordLength FROM usedWords;'
    else:
        print('Something went wrong with arguments to DB')
        cursor.close()
        conn.close()
        quit()
    cursor.execute(sql_statement)
    lengths_of_words:List[int] = sorted([x[0] for x in cursor.fetchall()])
    cursor.close()
    conn.close()
    return lengths_of_words

def reset_usedWords_table() -> None:
    '''Moves all of the contents in the usedWords table to the possibleWords table and deletes the contents of usedWords.'''
    conn = sqlite3.connect(DB_LOCATION)
    cursor = conn.cursor()
    sql_statement = 'SELECT * FROM usedWords;'
    cursor.execute(sql_statement)
    all_rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for word_info in all_rows:
        move_word_to_table(word_info=word_info, new_table='possibleWords')

def update_scoreboard(user_name:str, win:bool, word:str, num_guesses:int) -> None:
    '''Updates the scoreboard table to include the details about the game.'''
    conn = sqlite3.connect(DB_LOCATION)
    cursor = conn.cursor()
    sql_statement = 'INSERT INTO scoreboard (user, win, word, numGuesses) VALUES (?, ?, ?, ?);'
    cursor.execute(sql_statement, (user_name, win, word, num_guesses))
    conn.commit()
    cursor.close()
    conn.close()

@time_it
def main():
    lengths = select_all_word_lengths('possibleWords')
    for i in range(10000):
        random_index = randint(0, len(lengths)-1)
        word_length = lengths[random_index]
        word_info = select_random_word('possibleWords', word_length=word_length)
        if not word_info:
            print(f'No more words with length : {word_length}')
            continue
        word = word_info[1]
        print(', '.join([str(i) for i in word_info]))
        move_word_to_table(word_info, new_table='usedWords')
        if randint(0, 9) > 6:
            if randint(1,1000) == 1:
                update_scoreboard(user_name='bryan', win=True, word=word, num_guesses=1)
            else:
                update_scoreboard(user_name='bryan', win=True, word=word, num_guesses=randint(2,6))
        else:
            update_scoreboard(user_name='bryan', win=False, word=word, num_guesses=6)
    # reset_usedWords_table()

if __name__ == "__main__":
    main()