from session import session as _session
import models as _models
from insert_values_into_db import ID_list
# from datetime import date, datetime
from main import app


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! DIDN'T WORK
imported_ID_List = ID_list
# ACTOR
@app.post("generate_actor_values", tags=["actor"])
async def generate_actor_values(quantity_actor: int):
    actor_list = []
    index = 1
    age = 25
    while index != quantity_actor:
        if index in ID_list:
            index += 1
            quantity_actor += 1
            continue
        Name_surname = f"Name Number {str(index)}"
        rank = f"Rank Number {str(index)}"
        if index % 10 == 0:
            age += 8
        object = _models.actor(id = index, Name_Surname = Name_surname,
                    rank = rank, age = age, gender = "Male", ampula = "Some Ampula") 
        actor_list.append(object)
        index += 1

    if len(actor_list) != 0:
        _session.add_all(actor_list)
        _session.commit()
    else:
        return("ACTOR: NO VALUE ADDED")



# POSTANOVKA
@app.post("generate_postanovka_values", tags=["postanovka"])
async def generate_postanovka_values(quantity_postanovka: int):
    postanovka_list = []
    index = 1
    start_role = '2022/10/05'
    stop_role = '2022/10/05'
    group_number = 1
    date_of = '2022/10/05'
    while index != quantity_postanovka:
        if index in imported_ID_List:
            index += 1
            quantity_postanovka += 1
            continue
        role = f"Role Rumber{index}"
        object = _models.postanovka(id = index, start_role = start_role, 
                        stop_role = stop_role, role_type = role, group_number = group_number, 
                        director = "ROBERT B. WEIDE", date_of = date_of)
        postanovka_list.append(object)
        index += 1

    if len(postanovka_list) != 0:
        _session.add_all(postanovka_list)
        _session.commit()
    else:
        print("POSTANOVKA: NO VALUE ADDED")


# ROLE
@app.post("generate_role_values", tags=["role"])
async def generate_role_values(quantity_role: int):
    role_list = []
    index = 1
    while index != quantity_role:
        if index in imported_ID_List:
            index += 1
            quantity_role += 1
            continue
        name = f"Name Number {index}"
        piesa = f"Piesa Number {index}"
        object = _models.role(id = index, name = name, ampula = "Some Ampula", piesa = piesa, gender = "Male")
        role_list.append(object)
        index += 1

    if len(role_list) != 0:
        _session.add_all(role_list)
        _session.commit()
    else:
        print("ROLE: NO VALUE ADDED")

print("Generated Successfully")