from pydantic import BaseModel
from functools import cached_property
from glue_jupyter import JupyterApplication
from glue.core import DataCollection, Session
import solara


class BaseState(BaseModel):
    def as_dict(self):
        return self.model_dump()

    def update(self, new):
        return self.model_copy(update=new)


class Student(BaseModel):
    id: int = None


class Classroom(BaseModel):
    class_info: dict | None = {}
    size: int = 0


class Speech(BaseModel):
    pitch: int = 0
    rate: int = 0
    autoread: bool = False
    voice: str = ""


class BaseLocalState(BaseState):
    debug_mode: bool = False
    title: str
    story_id: str


class GlobalState(BaseState):
    drawer: bool = True
    speed_menu: bool = False
    loading_status_message: str = ""
    student: Student = Student()
    classroom: Classroom = Classroom()
    update_db: bool = True
    show_team_interface: bool = False
    allow_advancing: bool = True
    speech: Speech = Speech()
    piggybank_total: int = 0

    @cached_property
    def _glue_app(self) -> JupyterApplication:
        return JupyterApplication()

    @cached_property
    def glue_data_collection(self) -> DataCollection:
        return self._glue_app.data_collection

    @cached_property
    def glue_session(self) -> Session:
        return self._glue_app.session


GLOBAL_STATE = solara.reactive(GlobalState())
