import psycopg2
from psycopg2 import sql

# that's just training of usage...
print('sql-program started')

try:
    connection = psycopg2.connect(
        host="localhost",   # server address, localhost as default
        database="postgres",  # interested db, postgres as default
        user="postgres",    # postgres as default
        password="1111"   # password
    )

    cursor = connection.cursor() # cursor for executing sql requests

    # creation of table with SERIAL ID
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS happiness_rating (
        country_id SERIAL PRIMARY KEY,  -- SERIAL ID 
        name VARCHAR(100),
        continent VARCHAR(100)
    );
    '''
    cursor.execute(create_table_query)
    connection.commit()  # committing database changes

    # insertion and obtaining some string and returning ID
    insert_query = '''INSERT INTO happiness_rating (name, continent) VALUES (%s, %s) RETURNING country_id; '''
    cursor.execute(insert_query, ('Russia', 'Asia'))
    last_inserted_id = cursor.fetchone()[0]  # ID of the last inserted element
    connection.commit()  # approve commits

    print(f"ID of the last inserted element: {last_inserted_id}")

    # multistrings requests insertion
    multi_insert_query = ''' INSERT INTO happiness_rating (name, continent) VALUES (%s, %s); '''
    students_data = [
        ('Rohan', 'Rohan valley'),
        ('Mordor', 'Rune seaside'),
        ('Gondor', 'Nearest east')
    ]
    cursor.executemany(multi_insert_query, students_data) # insert 3 strings into the db
    connection.commit()

    # construction of the request and obtaining satisfying data from the database
    select_query = ''' SELECT * FROM happiness_rating; '''
    cursor.execute(select_query)
    rows = cursor.fetchall()

    # output the resutls as table
    print(f"{'ID SERIAL':<10}{'Name':<20}{'Continent':<30}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<10}{row[1]:<20}{row[2]:<30}")

except Exception as error:
    print(f"Ошибка при работе с PostgreSQL: {error}")


if connection: # if we didn't stop in advance
    cursor.close()
    connection.close()
    print(f'connection to database is over. the program closed')
