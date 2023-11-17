import psycopg2

conn = psycopg2.connect(dbname="opera", user="admin", password="secret", host="localhost")

cursor = conn.cursor()
# with open("/home/voyager/Visual_Studio/RAU/DB_Project/actress_insert_values.txt", 'r') as file1:
#     for line in file1:
#         data = line.split()
#         id = data[0]
#         name_surname = data[1] + ' ' + data[2]
#         rank = data[3]
#         age = data[4]
#         gender = data[5]
#         ampula = data[6]
#         sql = f"INSERT INTO actor (id, name_surname, rank, age, gender, ampula) VALUES ({id}, '{name_surname}', '{rank}'," \
#               f"{age}, '{gender}', '{ampula}')"
#         cursor.execute(sql)


# with open("/home/voyager/Visual_Studio/RAU/DB_Project/postanovka_insert_values.txt", 'r') as file2:
#     for line in file2:
#         data = line.split()
#         my_id = data[0]
#         start_role = data[1]
#         stop_role = data[2]
#         role_type = data[3]
#         group_number = data[4]
#         director = data[5]
#         date_of = data[6]
#         sql = f"INSERT INTO postanovka (id, start_role, stop_role, role_type, group_number, director, date_of)" \
#               f"VALUES ({my_id}, '{start_role}', '{stop_role}', '{role_type}', {group_number}, '{director}', '{date_of}')"
#         cursor.execute(sql)


with open("/home/voyager/Visual_Studio/RAU/DB_Project/role_insert_values.txt", 'r') as file3:
    for line in file3:
        data = line.split()
        my_id = data[0]
        name = data[1]
        ampula = data[2]
        piesa = data[3]
        gender = data[4]
        sql = f"INSERT INTO role (id, name, ampula, piesa, gender)" \
              f"VALUES ({my_id}, '{name}', '{ampula}', '{piesa}', '{gender}')"
        cursor.execute(sql)

conn.commit()
cursor.close()
conn.close()
