import solara
import dataclasses
from typing import Optional, cast, Dict, Union
from solara import Reactive
import httpx
from solara_enterprise import auth

from glue_jupyter.app import JupyterApplication
from glue.core.data_collection import DataCollection
from glue.core.session import Session
from .utils import request_session


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclasses.dataclass(frozen=True)
class HubUserInfo:
    name: Reactive[str] = dataclasses.field(default=Reactive("No message"))


@dataclasses.dataclass(frozen=True)
class Student:
    id: Reactive[int] = dataclasses.field(default=Reactive(0))
    size: Reactive[int] = dataclasses.field(default=Reactive(0))


@dataclasses.dataclass(frozen=True)
class Classroom:
    id: Reactive[int] = dataclasses.field(default=Reactive(0))
    size: Reactive[int] = dataclasses.field(default=Reactive(0))


@dataclasses.dataclass(frozen=True)
class Speech:
    pitch: Reactive[int] = dataclasses.field(default=Reactive(0))
    rate: Reactive[int] = dataclasses.field(default=Reactive(0))
    autoread: Reactive[bool] = dataclasses.field(default=Reactive(False))
    voice: Reactive[cast(Optional[str], None)] = dataclasses.field(
        default=Reactive(cast(Optional[str], None))
    )


@dataclasses.dataclass()
class GlobalState:
    drawer: Reactive[bool] = dataclasses.field(default=Reactive(False))
    speech_menu: Reactive[bool] = dataclasses.field(default=Reactive(False))
    loading_status_message: Reactive[str] = dataclasses.field(
        default=Reactive("No message")
    )
    student: Student = dataclasses.field(default_factory=Student)
    classroom: Classroom = dataclasses.field(default_factory=Classroom)
    update_db: Reactive[bool] = dataclasses.field(default=Reactive(False))
    show_team_interface: Reactive[bool] = dataclasses.field(default=Reactive(False))
    allow_advancing: Reactive[bool] = dataclasses.field(default=Reactive(True))
    speech: Speech = dataclasses.field(default_factory=Speech)

    def __post_init__(self):
        # self._data_collection = DataCollection()
        # self._session = Session(data_collection=self._data_collection, application=None)
        self._glue_app = JupyterApplication()

        self._request_session = request_session()

    @property
    def data_collection(self):
        """
        Underlying glue-jupyter application data collection instance.
        """
        return self._glue_app.data_collection

    @property
    def session(self):
        """
        Underlying glue-jupyter application data collection instance.
        """
        return self._glue_app.session

    @property
    def hub(self):
        return self._glue_app.session.hub

    @property
    def request_session(self):
        return self._request_session
