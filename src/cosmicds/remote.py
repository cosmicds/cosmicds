from solara_enterprise import auth
import hashlib
import os
from requests import Session
from typing import Optional
from functools import cached_property

from .state import GLOBAL_STATE, BaseLocalState, BaseState, GlobalState, Student
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

        if not ("cds/email" in userinfo or "cds/name" in userinfo):
            logger.error("Failed to create hash: not authentication information.")
            return

        user_ref = userinfo.get("cds/email", userinfo["cds/name"])

        hashed = hashlib.sha1(
            (user_ref + os.environ["SOLARA_SESSION_SECRET_KEY"]).encode()
        ).hexdigest()

        return hashed

    @property
    def user_exists(self):
        r = self.request_session.get(f"{self.API_URL}/student/{self.hashed_user}")
        return r.json()["student"] is not None

    
    @property
    def is_educator(self):
        r = self.request_session.get(
            f"{self.API_URL}/educators/{self.hashed_user}"
        )
        return r.json()["educator"] is not None
    

    def update_class_size(self, state: Reactive[GlobalState]):
        class_id = state.value.classroom.class_info["id"]
        size_json = self.request_session.get(
            f"{self.API_URL}/classes/size/{class_id}"
        ).json()
        Ref(state.fields.classroom.size).set(size_json["size"])

    def load_user_info(self, story_name: str, state: Reactive[GlobalState]):
        student_json = self.request_session.get(
            f"{self.API_URL}/student/{self.hashed_user}"
        ).json()["student"]
        sid = student_json["id"]

        class_json = self.request_session.get(
            f"{self.API_URL}/class-for-student-story/{sid}/{story_name}"
        ).json()

        Ref(state.fields.student.id).set(sid)
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
            f"{self.API_URL}/students/create",
            json={
                "username": self.hashed_user,
                "password": "",
                "institution": "",
                "email": f"{self.hashed_user}",
                "age": 0,
                "gender": "undefined",
                "classroom_code": class_code,
            },
        )

        if r.status_code != 201:
            logger.error("Failed to create new user.")
            return

        logger.info(
            "Created new user `%s` with class code '%s'.",
            self.hashed_user,
            class_code,
        )

        self.load_user_info(story_name, state)

    def put_stage_state(
        self,
        global_state: Reactive[GlobalState],
        local_state: Reactive[BaseLocalState],
        component_state: Reactive[BaseState],
    ):
        raise NotImplementedError()

    def get_stage_state(
        self,
        global_state: Reactive[GlobalState],
        local_state: Reactive[BaseLocalState],
        component_state: Reactive[BaseState],
    ) -> BaseState | None:

        if not global_state.value.update_db or self.is_educator:
            logger.info("Skipping retrieval of Component state.")
            return component_state.value

        stage_json = (
            self.request_session.get(
                f"{self.API_URL}/stage-state/{global_state.value.student.id}/"
                f"{local_state.value.story_id}/{component_state.value.stage_id}"
            )
            .json()
            .get("state", None)
        )

        if stage_json is None:
            logger.error(
                "Failed to retrieve stage state for story `%s` for user `%s`.",
                local_state.value.story_id,
                global_state.value.student.id,
            )
            return

        component_state.set(component_state.value.__class__(**stage_json))

        logger.info("Updated component state from database.")

        return component_state.value

    def delete_stage_state(
        self,
        global_state: Reactive[GlobalState],
        local_state: Reactive[BaseLocalState],
        component_state: Reactive[BaseState],
    ):
        if not global_state.value.update_db or self.is_educator:
            logger.info("Skipping deletion of stage state.")
            return

        r = self.request_session.delete(
            f"{self.API_URL}/stage-state/{global_state.value.student.id}/"
            f"{local_state.value.story_id}/{component_state.value.stage_id}"
        )

        if r.status_code != 200:
            logger.error(
                "Stage state for stage `%s`, story `%s` user `%s` did not exist in database.",
                component_state.value.stage_id,
                local_state.value.story_id,
                global_state.value.student.id,
            )
            return

        result = r.json()
        if not result.get("success", False):
            logger.error(
                "Error deleting stage state for stage `%s`, story `%s` user `%s`.",
                component_state.value.stage_id,
                local_state.value.story_id,
                global_state.value.student.id,
            )
            return

    def get_app_story_states(
        self, global_state: Reactive[GlobalState], local_state: Reactive[BaseLocalState]
    ) -> BaseLocalState | None:
        if global_state.value.update_db and not self.is_educator:

            story_json = (
                self.request_session.get(
                    f"{self.API_URL}/story-state/{global_state.value.student.id}/"
                    f"{local_state.value.story_id}"
                )
                .json()
                .get("state", None)
            )

            if story_json is None:
                logger.error(f"Failed to retrieve state for story {local_state.value.story_id} for user {global_state.value.student.id}.")
                return

        else:
            logger.info("Skipping retrieval of Global and Local states.")
            story_json = {
                "app": GlobalState(
                    student=GLOBAL_STATE.value.student, 
                    show_team_interface = GLOBAL_STATE.value.show_team_interface, 
                    classroom = GLOBAL_STATE.value.classroom,
                    educator = GLOBAL_STATE.value.educator,
                    update_db = GLOBAL_STATE.value.update_db,
                    ).model_dump(),
                "story": type(local_state.value)(
                    title=local_state.value.title, story_id=local_state.value.story_id
                ).as_dict(), # type: ignore
            }

        global_state_json = story_json.get("app", {})
        BaseAPI._update_state(global_state, global_state_json)

        local_state_json = story_json.get("story", {})
        BaseAPI._update_state(local_state, local_state_json)

        logger.info("Updated local state from database.")

        return local_state.value

    def put_story_state(
        self,
        global_state: Reactive[GlobalState],
        local_state: Reactive[BaseLocalState],
    ):
        raise NotImplementedError()

    def ignore_student_for_story(
        self,
        story_name: str,
        student_id: Optional[int] = None,
        ignore: bool = True,
    ):
        stu_id = student_id or self.hashed_user

        r = self.request_session.put(
            f"{self.API_URL}/students/ignore/{stu_id}/{story_name}",
            json={
                "ignore": ignore,
            }
        )

        if r.status_code != 200:
            logger.error(f"Failed to update ignored status for student {stu_id} for story {story_name}")
            return

        logger.info(f"Set student {stu_id}'s ignored status to {ignore} for story {story_name}")


    @staticmethod
    def clear_user(state: Reactive[GlobalState]):
        Ref(state.fields.student.id).set(0)
        Ref(state.fields.classroom.class_info).set({})
        Ref(state.fields.classroom.size).set(0)

    @staticmethod
    def _update_state(state: Reactive[BaseState], data: dict):
        new_state = state.value.__class__(**data)
        state.value.__dict__.update(new_state.__dict__)


BASE_API = BaseAPI()
