from fastapi import FastAPI
from session import session as _session
import models as _models

app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "First FastAPI app"}

@app.post("/create")
async def create_todo(id : int, text: str, is_complete: bool = False):
    todo = _models.Todo(id=id, text=text, is_done=is_complete)
    _session.add(todo)
    _session.commit()
    return {"todo added": todo.text}


@app.get("/")
async def get_all_todos():
    todos_query = _session.query(_models.Todo)
    return todos_query.all()


@app.get("/done")
async def list_done_todos():
    todos_query = _session.query(_models.Todo)
    done_todos_query = todos_query.filter(_models.Todo.is_done==True)
    return done_todos_query.all()


@app.put("/update/{id}")
async def update_todo(
    id: int,
    new_text: str = "",
    is_complete: bool = False
):
    
    todo_query = _session.query(_models.Todo).filter(_models.Todo.id==id)
    todo = todo_query.first()
    if new_text:
        todo.text = new_text
    todo.is_done = is_complete
    _session.add(todo)
    _session.commit()


@app.delete("/delete/{id}")
async def delete_todo(id: int):
    todo = _session.query(_models.Todo).filter(_models.Todo.id==id).first() # Todo object
    _session.delete(todo)
    _session.commit()
    return {"todo deleted": todo.text, "ID": id}