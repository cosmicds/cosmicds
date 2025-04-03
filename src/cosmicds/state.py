import os
from pydantic import BaseModel, Field
from functools import cached_property
from glue_jupyter import JupyterApplication
from glue.core import DataCollection, Session
import solara
from glue.core import Data, DataCollection


update_db_init = True
# CDS_DISABLE_DB must exist, and have the value 'true' to disable writing to the database
if 'CDS_DISABLE_DB' in os.environ:
    # check if it has a value and if it True
    cds_disable_db = os.getenv("CDS_DISABLE_DB")
    if cds_disable_db.lower() == 'true':
        print("Disabling database updates.")
        update_db_init = False
else:
    print("Database updates enabled.")

debug_mode_init = False
# CDS_DEBUG_MODE must exist, and have the value 'true' to enable debug mode
if 'CDS_DEBUG_MODE' in os.environ:
    # check if it has a value and if it True
    cds_debug_mode = os.getenv("CDS_DEBUG_MODE")
    if cds_debug_mode.lower() == 'true':
        print("Debug mode enabled.")
        debug_mode_init = True
else:
    print("Debug mode disabled.")

show_team_interface_init = False
# CDS_SHOW_TEAM_INTERFACE must exist, and have the value 'true' to enable team interface
if 'CDS_SHOW_TEAM_INTERFACE' in os.environ:
    # check if it has a value and if it True
    cds_show_team_interface = os.getenv("CDS_SHOW_TEAM_INTERFACE")
    if cds_show_team_interface.lower() == 'true':
        print("Team interface enabled.")
        show_team_interface_init = True
else:
    print("Team interface disabled.")

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
    pitch: float = 1.0
    rate: float = 1.0
    autoread: bool = False
    voice: str | None = None


class BaseLocalState(BaseState):
    debug_mode: bool = Field(debug_mode_init, exclude=True)
    title: str
    story_id: str
    piggybank_total: int = 0
    max_route_index: int | None = None


class GlobalState(BaseState):
    drawer: bool = True
    speed_menu: bool = False
    loading_status_message: str = ""
    student: Student = Student()
    classroom: Classroom = Classroom()
    update_db: bool = Field(update_db_init, exclude=True)
    show_team_interface: bool = Field(show_team_interface_init, exclude=True)
    allow_advancing: bool = True
    speech: Speech = Speech()
    educator: bool = False

    @cached_property
    def _glue_app(self) -> JupyterApplication:
        return JupyterApplication()

    @cached_property
    def glue_data_collection(self) -> DataCollection:
        return self._glue_app.data_collection

    @cached_property
    def glue_session(self) -> Session:
        return self._glue_app.session
    
    def add_or_update_data(self, data: Data):
        if data.label in self.glue_data_collection:
            existing = self.glue_data_collection[data.label]
            existing.update_values_from_data(data)
            return existing
        else:
            self.glue_data_collection.append(data)
            return data


GLOBAL_STATE = solara.reactive(GlobalState())
