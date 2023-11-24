from fastapi import FastAPI
from session import session as _session
import models as _models
from requests import HTTPError
from sqlalchemy import DateTime
from datetime import datetime
from insert_values_into_db import ID_list

app = FastAPI()

# ACTOR

@app.post("/create_actor", tags=["actor"])
async def create_actor(id : int, Name_Surname: str, age: int, rank: str = "", gender: str = "", 
                      ampula: str = ""): # sort names how you want, there is no difference, it's for front-end, we don't giva a s#it about front
    object = _models.actor(id=id, Name_Surname=Name_Surname, rank=rank, age=age, gender=gender, 
                         ampula=ampula)
    _session.add(object)
    _session.commit()
    return f"actor added: {object.Name_Surname}"


@app.get("/", tags=["actor"])
async def get_all_actors():
    actors_query = _session.query(_models.actor)
    return actors_query.all()


# @app.get("/done") # SELECT EXAMPLE
# async def list_done_todos():
#     todos_query = _session.query(_models.actor)
#     done_todos_query = todos_query.filter(_models.actor.is_done==True)
#     return done_todos_query.all()


@app.put("/update/{id}", tags=["actor"])
async def actor_update(
    id: int,
    new_Name_Surname: str = "",
    new_rank: str = "",
    new_age: int = 0,
    new_gender: str = "",
    new_ampula: str = ""
):
    
    actor_object = _session.query(_models.actor).filter(_models.actor.id==id).first()
    if actor_object is None: # TEST THIS
        return "No Such ID"
    # if actor_object.id != id: # check if actor_object is not None
    #     print(f"id: {id} is not in use")
    #     return HTTPError
    if new_Name_Surname:
        actor_object.Name_Surname = new_Name_Surname
    if new_rank:
        actor_object.rank = new_rank
    if new_age != 0:
        actor_object.age = new_age
    if new_gender:
        actor_object.gender = new_gender
    if new_ampula:
        actor_object.ampula = new_ampula
    _session.add(actor_object)
    _session.commit()
    return "actor successfully updated"


@app.delete("/delete/{id}", tags=["actor"])
async def actor_delete(id: int):
    actor = _session.query(_models.actor).filter(_models.actor.id==id).first() # actor object
    if actor is not None:
        if _session.query(_models.postanovka).filter(_models.postanovka.id==id).first() is None:
            if _session.query(_models.role).filter(_models.role.id==id).first() is None:
                _session.delete(actor)
                _session.commit()
                return f"Actor deleted: {actor.Name_Surname}"
    else: # didn't worked, idk why
        # print(f"id: {id} Referenced so can't be deleted")
        # return HTTPError 
        return f"ID: {id} Referenced so can't be deleted"

    return HTTPError
    
    
    
    
# POSTANOVKA
@app.post("/create_postanovka", tags=["postanovka"], response_model=None)
async def create_postanovka(id : int, group_number: int = 0, start_role: DateTime = datetime.now(), stop_role: DateTime = datetime.now(), role_type: str = "",
                            director: str = "", date_of: DateTime = datetime.now()): # sort names how you want, there is no difference, it's for front-end, we don't giva a s#it about front
    object = _models.postanovka(id=id, start_role=start_role, stop_role=stop_role, role_type=role_type, group_number=group_number, 
                         director=director, date_of=date_of)
    _session.add(object)
    _session.commit()
    if role_type:
        return f"postanovka added: {object.role_type}"
    else:
        return f"postanovka added: ID = {object.id}"

@app.get("/", tags=["postanovka"])
async def get_all_postanovka():
    postanovka_query = _session.query(_models.postanovka)
    return postanovka_query.all()


@app.put("/update/{id}", tags=["postanovka"])
async def postanovka_update(
    id: int,
    new_group_number: int = 0,
    new_start_role: DateTime = datetime.now,
    new_stop_role: DateTime = datetime.now,
    new_role_type: str = "",
    new_director: str = "",
    new_date_of: DateTime = datetime.now
):
    
    postanovka_object = _session.query(_models.postanovka).filter(_models.postanovka.id==id).first()
    if postanovka_object is None: # TEST THIS
        return "No Such ID"
    # if actor_object.id != id: # check if actor_object is not None
    #     print(f"id: {id} is not in use")
    #     return HTTPError    
    if postanovka_object.id in ID_list:
        return f"ID: {id} is in use"
    if new_group_number:
        postanovka_object.group_number = new_group_number
    if new_start_role:
        postanovka_object.stop_role = new_start_role
    if new_stop_role != 0:
        postanovka_object.stop_role = new_stop_role
    if new_role_type:
        postanovka_object.role_type = new_role_type
    if new_director:
        postanovka_object.director = new_director
    if new_date_of:
        postanovka_object.date_of = new_date_of
    _session.add(postanovka_object)
    _session.commit()
    return "postanovka successfully updated"


@app.delete("/delete/{id}", tags=["postanovka"])
async def postanovka_delete(id: int):
    postanovka_object = _session.query(_models.postanovka).filter(_models.postanovka.id==id).first() # actor object
    if postanovka_object is not None:
        _session.delete(postanovka_object)
        _session.commit()
        return f"postanovka deleted: {postanovka_object.id}"
    else: return HTTPError(f"ID {id} is not in use, so can't be deleted") 






# ROLE

@app.post("/create_role", tags=["role"])
async def create_role(id : int, name: str = "", ampula: str = "", piesa: str = "", gender: str = ""): # sort names how you want, there is no difference, it's for front-end, we don't giva a s#it about front
    object = _models.role(id=id, name=name, ampula=ampula, piesa=piesa, gender=gender)
    _session.add(object)
    _session.commit()
    if name:
        return f"role added: {object.name}"
    else:
        return f"role added: ID = {object.id}"
    

@app.get("/", tags=["role"])
async def get_all_roles():
    role_query = _session.query(_models.role)
    return role_query.all()


@app.put("/update/{id}", tags=["role"])
async def role_update(
    id: int,
    new_name: str = "",
    new_ampula: str = "",
    new_piesa: str = "", 
    new_gender: str = ""
):
    
    role_object = _session.query(_models.role).filter(_models.role.id==id).first()
    if role_object is None: # TEST THIS
        return HTTPError("No Such ID")
    # if actor_object.id != id: # check if actor_object is not None
    #     print(f"id: {id} is not in use")
    #     return HTTPError    
    if role_object.id in ID_list:
        return f"ID: {id} is in use"
    if new_name:
        role_object.name = new_name
    if new_ampula:
        role_object.ampula = new_ampula
    if new_piesa != 0:
        role_object.piesa = new_piesa
    if new_gender:
        role_object.gender = new_gender
    _session.add(role_object)
    _session.commit()
    return "role successfully updated"


@app.delete("/delete/{id}", tags=["role"])
async def role_delete(id: int):
    role_object = _session.query(_models.role).filter(_models.role.id==id).first() # actor object
    if role_object is not None:
        _session.delete(role_object)
        _session.commit()
        return f"postanovka deleted: {role_object.id}"
    else: 
        return HTTPError(f"ID {id} is not in use, so can't be deleted") 


