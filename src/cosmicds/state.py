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
from .utils import request_session, API_URL, debounce


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseState:
    def as_dict(self):
        def _inner_dict(sub_comp):
            if isinstance(sub_comp, solara.toestand.Reactive):
                # TODO: we need to revisit the free response handling in the
                #  Hubble data story. Not sure what's going on there, but
                #  it's not clear why there's so many factories.
                if sub_comp.value.__class__.__name__ == "FreeResponseDict":
                    return {}

            if dataclasses.is_dataclass(sub_comp):
                return {
                    f.name: _inner_dict(getattr(sub_comp, f.name))
                    for f in dataclasses.fields(sub_comp)
                }

            return (
                sub_comp.value
                if isinstance(sub_comp, solara.toestand.Reactive)
                else sub_comp
            )

        return _inner_dict(self)

    def from_dict(self, d):
        def _inner_dict(dd, parent):
            for k, v in dd.items():
                attr = getattr(parent, k)

                if isinstance(attr, solara.toestand.Reactive):
                    attr.set(v)
                elif dataclasses.is_dataclass(attr):
                    _inner_dict(v, attr)

        _inner_dict(d, self)

    def _setup_database_write_listener(self, func):
        def _callback():
            func()

        def _inner_dict(sub_comp):
            if dataclasses.is_dataclass(sub_comp):
                return {
                    f.name: _inner_dict(getattr(sub_comp, f.name))
                    for f in dataclasses.fields(sub_comp)
                }

            if isinstance(sub_comp, solara.toestand.Reactive):
                sub_comp.subscribe_change(lambda *args: _callback())

        _inner_dict(self)


@dataclasses.dataclass(frozen=True)
class HubUserInfo:
    name: Reactive[str] = dataclasses.field(default=Reactive("No message"))


@dataclasses.dataclass(frozen=True)
class Student:
    id: Reactive[int] = dataclasses.field(default=Reactive(0))


@dataclasses.dataclass(frozen=True)
class Classroom:
    class_: Reactive[dict] = dataclasses.field(default=Reactive({}))
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
class GlobalState(BaseState):
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
            return

        username = hashlib.sha1(
            (user_ref + os.environ["SOLARA_SESSION_SECRET_KEY"]).encode()
        ).hexdigest()

        return username

    def _setup_user(self, story_name, class_code):
        if not auth.user.value or self.student.id.value:
            return

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
                    "email": f"{self.hashed_user}",
                    "age": 0,
                    "gender": "undefined",
                    "classroomCode": class_code,
                },
            )

            r = self.request_session.get(f"{API_URL}/student/{self.hashed_user}")
            student = r.json()["student"]
        else:
            print(f"Found user '{self.hashed_user}' in database.")

        self.student.id.set(student.get("id", 0))

        r = self.request_session.get(
            f"{API_URL}/class-for-student-story/{self.student.id.value}/{story_name}"
        )
        class_json = r.json()

        self.classroom.class_.set(class_json["class"])
        self.classroom.size.set(class_json["size"])

    def _clear_user(self):
        self.student.id.set(0)
        self.classroom.class_.set({})
        self.classroom.size.set(0)
