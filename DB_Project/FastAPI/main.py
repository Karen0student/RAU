from fastapi import FastAPI
from session import session as _session
import models as _models
from requests import HTTPError

app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "First FastAPI app"}

@app.post("/create_actor", tags=["actor"])
async def create_actor(id : int, Name_Surname: str, rank: str, age: int, gender: str, 
                      ampula: str):
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
    if actor_object.id != id: # check if actor_object is not None
        print(f"id: {id} is not in use")
        return HTTPError
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
    return "New actor successfully added"


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
        return f"id: {id} Referenced so can't be deleted"

    return HTTPError
    