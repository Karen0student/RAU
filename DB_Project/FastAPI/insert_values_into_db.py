import models as _models
from session import session as _session
# from main import _models
# from main import _session

actor_list = []
# ATTENTION !!! PATH MAY BE DIFFERENT, CORRECT THIS FOR FINAL SHOWCASE
with open("/home/voyager/Visual_Studio/DB_Project/postgres/backup/actress_insert_values.txt", 'r') as file1:
    for line in file1:
        data = line.split()
        object = _models.actor(id = data[0], Name_Surname = data[1] + ' ' + data[2],
            rank = data[3], age = data[4], gender = data[5], ampula = data[6])
        actor_list.append(object)


_session.add_all(actor_list)
_session.commit()



postanovka_list = []
with open("/home/voyager/Visual_Studio/DB_Project/postgres/backup/postanovka_insert_values.txt", 'r') as file2:
    for line in file2:
        data = line.split()
        object = _models.postanovka(id = data[0], start_role = data[1], stop_role = data[2],
            role_type = data[3], group_number = data[4], director = data[5], date_of = data[6])
        postanovka_list.append(object)


_session.add_all(postanovka_list)
_session.commit()



role_list = []
with open("/home/voyager/Visual_Studio/DB_Project/postgres/backup/role_insert_values.txt", 'r') as file3:
    for line in file3:
        data = line.split()
        object = _models.role(id = data[0], name = data[1], ampula = data[2], piesa = data[3], gender = data[4])
        role_list.append(object)


_session.add_all(role_list)
_session.commit()

# todo1 = _models.actor(id = 1, text="learn fastapi", is_done=True)
# todo2 = _models.actor(id = 2, text="learn django", is_done=True)

# _session.add_all([todo1, todo2])
# _session.commit()