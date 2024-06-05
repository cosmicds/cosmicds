import os
import hashlib
import solara
import dataclasses
from typing import Optional, cast, Dict, Union
from solara import Reactive
import httpx
from solara_enterprise import auth

from glue_jupyter.app import JupyterApplication
from glue.core.data_collection import DataCollection
from glue.core.session import Session
from .utils import request_session, API_URL


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

    @property
    def hashed_user(self):
        userinfo = auth.user.value["userinfo"]

        if "email" in userinfo or "name" in userinfo:
            user_ref = userinfo.get("email", userinfo["name"])
        else:
            # TODO: should be hidden on production
            solara.Markdown(f"Failed to hash \n\n{userinfo}")
            return

        username = hashlib.sha1(
            (user_ref + os.environ["SOLARA_SESSION_SECRET_KEY"]).encode()
        ).hexdigest()

        return username

    def _setup_user(self, class_code):
        # See if the user is actually in the database, otherwise create user
        r = self.request_session.get(f"{API_URL}/student/{self.hashed_user}")
        student = r.json()["student"]

        if student is None:
            print(
                f"User '{self.hashed_user}' not found in database. Creating "
                f"new user with class code '{class_code}'"
            )

            userinfo = auth.user.value["userinfo"]

            # Create new user based on username and class code
            r = self.request_session.post(
                f"{API_URL}/student-sign-up",
                json={
                    "username": self.hashed_user,
                    "password": "",
                    "institution": "",
                    "email": userinfo.get("email", ""),
                    "age": 0,
                    "gender": "undefined",
                    "classroomCode": class_code,
                },
            )
        else:
            print(f"Found user '{self.hashed_user}' in database.")


GLOBAL_STATE = GlobalState()
