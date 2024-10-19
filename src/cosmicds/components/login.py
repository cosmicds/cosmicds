import solara
import reacton.ipyvuetify as rv
from cosmicds.state import GLOBAL_STATE
from solara.lab import Ref
from solara_enterprise import auth
from cosmicds.utils import get_session_id
from solara import Reactive


def _save_to_cache(class_code: str, update_db: bool, debug_mode: bool):
    solara.cache.storage[f"cds-login-options-{get_session_id()}"] = {
        "class_code": class_code,
        "update_db": update_db,
        "debug_mode": debug_mode,
    }


@solara.component
def Login(
    active: Reactive[bool],
    class_code: Reactive[str],
    update_db: Reactive[bool],
    debug_mode: Reactive[bool],
):
    with rv.Dialog(
        v_model=active.value,
        max_width=600,
        # fullscreen=True,
        persistent=True,
        overlay_color="grey darken-2",
    ) as login:
        team_interface = Ref(GLOBAL_STATE.fields.show_team_interface)

        with rv.Card():
            with rv.CardText():
                with rv.Container(
                    class_="d-flex align-center flex-column justify-center"
                ):
                    solara.Image(
                        "/static/public/cosmicds_logo_transparent_for_dark_backgrounds.png",
                        classes=["mt-12"],
                    )
                    solara.Text(
                        "Hubble's Law Data Story", classes=["display-1", "py-12"]
                    )

                    solara.InputText(
                        label="Enter Class Code", value=class_code, continuous_update=True,
                    )

                    solara.Button(
                        "Sign in",
                        href=auth.get_login_url(),
                        disabled=not class_code.value,
                        outlined=False,
                        large=True,
                        color="success",
                        on_click=lambda: _save_to_cache(
                            class_code.value, update_db.value, debug_mode.value
                        ),
                        class_="mt-12",
                    )

    return login
