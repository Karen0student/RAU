import models as _models
from session import session as _session
# from main import _models
# from main import _session


todo1 = _models.Todo(id = 1, text="learn fastapi", is_done=True)
todo2 = _models.Todo(id = 2, text="learn django", is_done=True)

_session.add_all([todo1, todo2])
_session.commit()