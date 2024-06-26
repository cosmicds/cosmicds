from solara_enterprise import auth
import hashlib
import os
from requests import Session
from functools import cached_property
from .state import GlobalState
from solara import Reactive
from solara.lab import Ref
from cosmicds.logger import setup_logger

logger = setup_logger("API")


class BaseAPI:
    API_URL = "https://api.cosmicds.cfa.harvard.edu"

    @cached_property
    def request_session(self):
        """
        Returns a `requests.Session` object that has the relevant authorization
        parameters to interface with the CosmicDS API server (provided that
        environment variables are set correctly).
        """
        session = Session()
        session.headers.update({"Authorization": os.getenv("CDS_API_KEY")})
        return session

    @property
    def hashed_user(self):
        if auth.user.value is None:
            logger.error("Failed to create hash: user not authenticated.")
            return "User not authenticated"

        userinfo = auth.user.value.get("userinfo")

        if not ("email" in userinfo or "name" in userinfo):
            logger.error("Failed to create hash: not authentication information.")
            return

        user_ref = userinfo.get("email", userinfo["name"])

        hashed = hashlib.sha1(
            (user_ref + os.environ["SOLARA_SESSION_SECRET_KEY"]).encode()
        ).hexdigest()

        return hashed

    @property
    def user_exists(self):
        r = self.request_session.get(f"{self.API_URL}/student/{self.hashed_user}")
        return r.json()["student"] is not None

    def load_user_info(self, story_name: str, state: Reactive[GlobalState]):
        student_json = self.request_session.get(
            f"{self.API_URL}/student/{self.hashed_user}"
        ).json()["student"]

        class_json = self.request_session.get(
            f"{self.API_URL}/class-for-student-story/{state.value.student.id}/{story_name}"
        ).json()

        student_id = Ref(state.fields.student.id)
        student_id.set(student_json["id"])
        Ref(state.fields.classroom.class_info).set(class_json["class"])
        Ref(state.fields.classroom.size).set(class_json["size"])

        logger.info("Loaded user info for user `%s`.", state.value.student.id)

    def create_new_user(
        self, story_name: str, class_code: str, state: Reactive[GlobalState]
    ):
        r = self.request_session.get(f"{self.API_URL}/student/{self.hashed_user}")
        student = r.json()["student"]

        if student is not None:
            logger.error(
                "Failed to create user `%s`: user already exists.", self.hashed_user
            )
            return

        r = self.request_session.post(
            f"{self.API_URL}/student-sign-up",
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

        if r.status_code != 200:
            logger.error("Failed to create new user.")
            return

        logger.info(
            "Created new user `%s` with class code '%s'.",
            self.hashed_user,
            class_code,
        )

        self.load_user_info(story_name, state)

    @staticmethod
    def clear_user(state: Reactive[GlobalState]):
        Ref(state.fields.student.id).set(0)
        Ref(state.fields.classroom.class_info).set({})
        Ref(state.fields.classroom.size).set(0)


BASE_API = BaseAPI()
