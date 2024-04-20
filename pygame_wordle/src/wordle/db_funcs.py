import sqlite3
from typing import Tuple
from random import randint

def move_word_to_table(word_info:Tuple[int, str, int], new_table:str) -> None:
    '''
        Copy word entry into a new table, then remove it from the original table.
        Arguments:
            - word_info : tuple containing (word_id, word, word_length)
            - new_table (table you want to move to) : 'possible_words' or 'used_words'
    '''

    def delete_word_from_table(conn:sqlite3.Connection, word_info:Tuple[int, str, int], old_table:str) -> None:
        '''
            Delete word entry from table.
            Arguments:
                - conn : sqlite3 connection object
                - word_info : tuple containing (word_id, word, word_length)
                - old_table (table you want to delete from) : 'possible_words' or 'used_words'
        '''
        word_id = word_info[0]
        cursor = conn.cursor()
        if old_table == 'possible_words':
            sql_statement = 'DELETE FROM possible_words WHERE id = ?;'
        elif old_table == 'used_words':
            sql_statement = 'DELETE FROM used_words WHERE id = ?;'
        else:
            print('Something went wrong with arguments to DB')
            cursor.close()
            conn.close()
            quit()
        cursor.execute(sql_statement, (word_id,))
        conn.commit()
        cursor.close()

    conn = sqlite3.connect('../wordle/wordle_words.db')
    cursor = conn.cursor()
    if new_table == 'possible_words':
        old_table = 'used_words'
        sql_statement = 'INSERT INTO possible_words (id, word, wordLength) VALUES (?, ?, ?);'
    elif new_table == 'used_words':
        old_table = 'possible_words'
        sql_statement = 'INSERT INTO used_words (id, word, wordLength) VALUES (?, ?, ?);'
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
            - table (table you want to query) : 'possible_words' or 'used_words'
            - word_length : integer, must be a valid length, but will be provided by selecting a button on the main menu
    '''
    conn = sqlite3.connect('../wordle/wordle_words.db')
    cursor = conn.cursor()
    if table == 'possible_words':
        sql_statement = 'SELECT * FROM possible_words WHERE wordLength = ?;'
    elif table == 'used_words':
        sql_statement = 'SELECT * FROM used_words WHERE wordLength = ?;'
    else:
        print('Something went wrong with arguments to DB')
        cursor.close()
        conn.close()
        quit()
    cursor.execute(sql_statement, (word_length,))
    all_rows = cursor.fetchall()
    cursor.close()
    conn.close()
    random_word_index = randint(0, len(all_rows)-1)
    return all_rows[random_word_index]

def select_all_word_lengths(table:str):
    '''
        Query a table for distinct values in the wordLength column. returns a list of valid word lengths in the table.
        Arguments:
            - table (table you want to query) : 'possible_words' or 'used_words'
    '''
    conn = sqlite3.connect('../wordle/wordle_words.db')
    cursor = conn.cursor()
    if table == 'possible_words':
        sql_statement = 'SELECT DISTINCT wordLength FROM possible_words;'
    elif table == 'used_words':
        sql_statement = 'SELECT DISTINCT wordLength FROM used_words;'
    else:
        print('Something went wrong with arguments to DB')
        cursor.close()
        conn.close()
        quit()
    cursor.execute(sql_statement)
    lengths_of_words = sorted([x[0] for x in cursor.fetchall()])
    cursor.close()
    conn.close()
    return lengths_of_words