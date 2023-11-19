import models as _models
from session import session as _session
import psycopg2
from psycopg2 import sql
#import main as _main
# from main import _models
# from main import _session
#actor_list_in_main = []

# CHECK IF VALUES ALREADY EXISTS
def get_table_columns(table_name, connection):
    cursor = connection.cursor()

    # Use the information_schema to get column details
    cursor.execute(f"select id from {table_name}")

    columns = cursor.fetchall()
    string_values = [int(column[0]) for column in columns]
    cursor.close()
    return string_values


def check_if_value_exists(table_name):
    # Connect to the existing 'session' database
    connection = psycopg2.connect(
        dbname='opera',
        user='admin',
        password='secret',
        host='localhost',
        port='5432'
    )

    try:
        # Get table columns
        columns = get_table_columns(table_name, connection) # lists
    except Exception as e:
        print(f"Error: {e}")
    
    connection.close()
    return columns
    

ID_list = check_if_value_exists("actor") # only actor.id because it got references from others id's


actor_list = []
# print(f"ACTOR_CHECK_LIST: {ID_list}")
# ATTENTION !!! PATH MAY BE DIFFERENT, CORRECT THIS FOR FINAL SHOWCASE
with open("/home/voyager/Visual_Studio/DB_Project/postgres/backup/actress_insert_values.txt", 'r') as file1:
    for line in file1:
        data = line.split()
        check_value = int(data[0])
        if check_value in ID_list: 
            print(f"id: {check_value} Already in use")
            continue
        else:
            object = _models.actor(id = int(data[0]), Name_Surname = data[1] + ' ' + data[2],
                rank = data[3], age = int(data[4]), gender = data[5], ampula = data[6]) 
            actor_list.append(object)
        

# print(f"ACTOR_LIST: {actor_list}")
if len(actor_list) != 0:
    _session.add_all(actor_list)
    _session.commit()
        


postanovka_list = []
# print(f"POSTANOVKA_CHECK_LIST: {postanovka_check_list}")
with open("/home/voyager/Visual_Studio/DB_Project/postgres/backup/postanovka_insert_values.txt", 'r') as file2:
    for line in file2:
        data = line.split()
        check_value = int(data[0])
        if check_value in ID_list: 
            print(f"id: {check_value} Already in use")
            continue
        else:
            object = _models.postanovka(id = int(data[0]), start_role = data[1], 
                stop_role = data[2], role_type = data[3], group_number = int(data[4]), 
                director = data[5], date_of = data[6])
            postanovka_list.append(object)

# print(f"POSTANOVKA_LIST: {postanovka_list}")
if len(postanovka_list) != 0:
    _session.add_all(postanovka_list)
    _session.commit()



role_list = []
# print(f"ROLE_CHECK_LIST: {role_check_list}")
with open("/home/voyager/Visual_Studio/DB_Project/postgres/backup/role_insert_values.txt", 'r') as file3:
    for line in file3:
        data = line.split()
        check_value = int(data[0])
        if check_value in ID_list: 
            print(f"id: {check_value} Already in use")
            continue
        else:
            object = _models.role(id = data[0], name = data[1], ampula = data[2], piesa = data[3], gender = data[4])
            role_list.append(object)

# print(f"ROLE_LIST: {role_list}")
if len(role_list) != 0:
    _session.add_all(role_list)
    _session.commit()

# todo1 = _models.actor(id = 1, text="learn fastapi", is_done=True)
# todo2 = _models.actor(id = 2, text="learn django", is_done=True)

# _session.add_all([todo1, todo2])
# _session.commit()

# connection.close()