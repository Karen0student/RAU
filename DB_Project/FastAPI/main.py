from fastapi import FastAPI, HTTPException, status
from session import session as _session
import models as _models
# from requests import HTTPError
# from werkzeug.exceptions import HTTPException
# from sqlalchemy import DateTime
from datetime import datetime, date
# from insert_values_into_db import ID_list
from fastapi import Query

app = FastAPI()

# ACTOR
# imported_ID_List = ID_list
@app.post("/create_actor", tags=["actor"])
async def create_actor(actor_id : int, Name_Surname: str, age: int, rank: str = "", gender: str = "", 
                      ampula: str = ""): # sort names how you want, there is no difference, it's for front-end, we don't giva a s#it about front
    check_actor_id = _session.query(_models.actor).filter(_models.actor.id==actor_id).first()
    if check_actor_id is None:
        object = _models.actor(id=actor_id, Name_Surname=Name_Surname, rank=rank, age=age, gender=gender, 
                            ampula=ampula)
        _session.add(object)
        _session.commit()
        return f"actor added: {object.Name_Surname}"
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID IN USE, CHANGE THE ID")


@app.get("/get_actor", tags=["actor"])
async def get_all_actors(skip : int = Query(0, ge=0), limit: int = Query(100)):
    actors_query = _session.query(_models.actor).offset(skip).limit(limit)
    return actors_query.all()


# @app.get("/done") # SELECT EXAMPLE
# async def list_done_todos():
#     todos_query = _session.query(_models.actor)
#     done_todos_query = todos_query.filter(_models.actor.is_done==True)
#     return done_todos_query.all()


@app.put("/update/{actor_id}", tags=["actor"])
async def actor_update(
    actor_id: int,
    new_Name_Surname: str = "",
    new_rank: str = "",
    new_age: int = 0,
    new_gender: str = "",
    new_ampula: str = ""
):
    
    actor_object = _session.query(_models.actor).filter(_models.actor.id==actor_id).first()
    if actor_object is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such ID")
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


@app.delete("/delete/{actor_id}", tags=["actor"])
async def actor_delete(actor_id: int):
    actor = _session.query(_models.actor).filter(_models.actor.id==actor_id).first() # actor object
    if actor is not None:
        if _session.query(_models.postanovka).filter(_models.postanovka.id==actor_id).first() is None:
            if _session.query(_models.role).filter(_models.role.id==actor_id).first() is None:
                _session.delete(actor)
                _session.commit()
                return f"Actor deleted: {actor.Name_Surname}"
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} Referenced so can't be deleted")

    
    
    

# POSTANOVKA
@app.post("/create_postanovka", tags=["postanovka"])
async def create_postanovka(postanovka_id : int, start_role: date = datetime.now().strftime("%Y-%m-%d"), stop_role: date = datetime.now().strftime("%Y-%m-%d"), date_of: date = datetime.now().strftime("%Y-%m-%d"),
                            group_number: int = 0, role_type: str = "", director: str = ""): # sort names how you want, there is no difference, it's for front-end, we don't giva a s#it about front
    if _session.query(_models.actor).filter(_models.actor.id == postanovka_id).first() is not None: # if found id in actor.id
        if _session.query(_models.postanovka).filter(_models.postanovka.id == postanovka_id).first() is None: # if not found id in postanovka.id
            object = _models.postanovka(id=postanovka_id, start_role=start_role, stop_role=stop_role, role_type=role_type, group_number=group_number, 
                                director=director, date_of=date_of) 
            _session.add(object)
            _session.commit()
        else: return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID IN USE, CHANGE THE ID")
        if role_type:
            return f"postanovka added: {object.role_type}"
        else:
            return f"postanovka added: ID = {object.id}"
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such ID in actor")


@app.get("/get_postanovka", tags=["postanovka"])
async def get_all_postanovka(skip : int = Query(0, ge=0), limit: int = Query(100)):
    postanovka_query = _session.query(_models.postanovka).offset(skip).limit(limit)
    return postanovka_query.all()


@app.put("/update_postanovka/{postanovka_id}", tags=["postanovka"])
async def postanovka_update(
    postanovka_id: int,
    new_group_number: int = 0,
    new_start_role: date = datetime.now().strftime("%Y-%m-%d"),
    new_stop_role: date = datetime.now().strftime("%Y-%m-%d"),
    new_role_type: str = "",
    new_director: str = "",
    new_date_of: date = datetime.now().strftime("%Y-%m-%d")
):
    
    postanovka_object = _session.query(_models.postanovka).filter(_models.postanovka.id==postanovka_id).first()
    if postanovka_object is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such ID")
    # if actor_object.id != id: # check if actor_object is not None
    #     print(f"id: {id} is not in use")
    #     return HTTPError     
    # if postanovka_object.id in ID_list:
    #     return f"ID: {id} is in use"
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


@app.delete("/delete_postanovka/{postanovka_id}", tags=["postanovka"])
async def postanovka_delete(postanovka_id: int):
    postanovka_object = _session.query(_models.postanovka).filter(_models.postanovka.id==postanovka_id).first() # actor object
    if postanovka_object is not None:
        _session.delete(postanovka_object)
        _session.commit()
        return f"postanovka deleted: {postanovka_object.id}"
    else: return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such ID") 




# ROLE

@app.post("/create_role", tags=["role"])
async def create_role(role_id : int, name: str = "", ampula: str = "", piesa: str = "", gender: str = ""): # sort names how you want, there is no difference, it's for front-end, we don't giva a s#it about front
    check_role_id_first = _session.query(_models.actor).filter(_models.actor.id == role_id).first()
    if check_role_id_first is not None:
        check_role_id_second = _session.query(_models.role).filter(_models.role.id == role_id).first()
        if check_role_id_second is None:
            object = _models.role(id=role_id, name=name, ampula=ampula, piesa=piesa, gender=gender)
            _session.add(object)
            _session.commit()
        else: return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID IN USE, CHANGE THE ID")
        if name:
            return f"role added: {object.name}"
        else:
            return f"role added: ID = {object.id}"
    else: return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID IN USE, CHANGE THE ID")
    

@app.get("/get_role", tags=["role"])
async def get_all_roles(skip : int = Query(0, ge=0), limit: int = Query(100)):
    role_query = _session.query(_models.role).offset(skip).limit(limit)
    return role_query.all()


@app.put("/update_role/{role_id}", tags=["role"])
async def role_update(
    role_id: int,
    new_name: str = "",
    new_ampula: str = "",
    new_piesa: str = "", 
    new_gender: str = ""
):
    
    role_object = _session.query(_models.role).filter(_models.role.id==role_id).first()
    if role_object is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such ID")
    # if actor_object.id != id: # check if actor_object is not None
    #     print(f"id: {id} is not in use")
    #     return HTTPError    
    # if role_object.id in imported_ID_List:
    #     return f"ID: {role_id} is in use"
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


@app.delete("/delete_role/{role_id}", tags=["role"])
async def role_delete(role_id: int):
    role_object = _session.query(_models.role).filter(_models.role.id==role_id).first() # actor object
    if role_object is not None:
        _session.delete(role_object)
        _session.commit()
        return f"role deleted: {role_object.id}"
    else: return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such ID") 




# VALUE GENERATORS

# ACTOR
@app.post("/generate_actor_values", tags=["actor"])
async def generate_actor_values(quantity_actor: int):
    flag_of_commition = False
    index = 1
    age = 25
    while index != quantity_actor:
        if _session.query(_models.actor).filter(_models.actor.id==index).first() is not None:
            index += 1
            quantity_actor += 1
            continue
        Name_surname = f"Name Number {str(index)}"
        rank = f"Rank Number {str(index)}"
        if index % 10 == 0:
            age += 8
        object = _models.actor(id = index, Name_Surname = Name_surname,
                    rank = rank, age = age, gender = "Male", ampula = "Some Ampula") 
        _session.add(object)
        _session.commit()
        flag_of_commition = True
        index += 1

    if flag_of_commition is False:
        return "NO VALUE GENERATED"        
    else:
        return "Seccessfully added values"



# POSTANOVKA
@app.post("/generate_postanovka_values", tags=["postanovka"])
async def generate_postanovka_values(quantity_postanovka: int):
    flag_of_commition = False
    index = 1
    start_role = '2022/10/05'
    stop_role = '2022/10/05'
    group_number = 1
    date_of = '2022/10/05'
    while index != quantity_postanovka:
        if _session.query(_models.actor).filter(_models.actor.id==index).first() is not None:        
            if _session.query(_models.postanovka).filter(_models.postanovka.id==index).first() is not None:
                index += 1
                quantity_postanovka += 1
                continue
        else: return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="REACHED LIMIT OF ACTOR ID's")        
        if index % 10 == 0:
            group_number += 1
        role = f"Role Rumber{index}"
        object = _models.postanovka(id = index, start_role = start_role, 
                        stop_role = stop_role, role_type = role, group_number = group_number, 
                        director = "ROBERT B. WEIDE", date_of = date_of)
        _session.add(object)
        _session.commit()
        flag_of_commition = True
        index += 1

    if flag_of_commition is False:
        return "NO VALUE GENERATED"
    else:
        return "Seccessfully added values"


# ROLE
@app.post("/generate_role_values", tags=["role"])
async def generate_role_values(quantity_role: int):
    flag_of_commition = False
    index = 1
    while index != quantity_role:
        if _session.query(_models.actor).filter(_models.actor.id==index).first() is not None: # if reached last index in actor, raise HTTPException
            if _session.query(_models.role).filter(_models.role.id==index).first() is not None:
                index += 1
                quantity_role += 1
                continue
        else: return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="REACHED LIMIT OF ACTOR ID's")
        name = f"Name Number {index}"
        piesa = f"Piesa Number {index}"
        object = _models.role(id = index, name = name, ampula = "Some Ampula", piesa = piesa, gender = "Male")
        _session.add(object)
        _session.commit()
        flag_of_commition = True
        index += 1
    
    if flag_of_commition is False:
        return "NO VALUE GENERATED"
    else:
        return "Seccessfully added values"





        
# GROUP
# from sqlalchemy import func # it's for counting something from table # func.count(<raw of table>)

@app.get("/actors_count_by_age_group", tags=["unique commands"])
async def get_actors_count_by_age_group():
    actors_count_query = (
        _session.query(_models.actor.gender, _models.actor.Name_Surname)
        .group_by(_models.actor.gender, _models.actor.Name_Surname).all())
    return [{"gender": gender, "Name_Surname": Name_Surname} for gender, Name_Surname in actors_count_query]



# JOIN

@app.get("/actors_and_roles_join", tags=["unique commands"])
async def get_actors_and_roles():
    actors_roles_query = _session.query(_models.actor).join(
        _models.role, _models.actor.gender == _models.role.gender)
    return actors_roles_query.all()


# SELECT WHERE


@app.get("/Select_from_actors_where", tags=["unique commands"])
async def get_actors_by_conditions(
    age: int = Query(..., description="Filter actors by age"),
    gender: str = Query(..., description="Filter actors by gender"),
):
    actors_query = _session.query(_models.actor).filter(
        (_models.actor.age == age) & (_models.actor.gender == gender))
    return actors_query.all()


# SORT (order by)

@app.get("/actors_sorted_by_age", tags=["unique commands"])
async def get_actors_sorted_by_age(
    sort_order: str = Query(..., description="Sort order (asc/desc)")
):
    sort_column = _models.actor.age
    if sort_order.lower() == "desc":
        sort_column = sort_column.desc()

    actors_query = _session.query(_models.actor).order_by(sort_column)
    return actors_query.all()


# UPDATE

@app.put("/update_actors_rank", tags=["unique commands"])
async def update_actors_rank(
    gender: str = Query(..., description="choose a gender"),
    new_age: int = Query(..., description="New age for the selected actors"),
):
    update_query = ( # () for a new line separation in IDE
        _session.query(_models.actor)
        .filter((_models.actor.gender==gender))
        .update({"age": new_age})
    )
    _session.commit()
    return f"{update_query} actors updated with new rank."