import datetime
import os
from warnings import filterwarnings
from importlib.metadata import PackageNotFoundError, version
from typing import Optional

import solara
from solara.alias import rv
from ipyvue import Html
from solara.lab import theme
from solara.server import settings
from solara.toestand import Ref
from solara_enterprise import auth
from solara import Reactive


from .state import GLOBAL_STATE, BaseLocalState, Speech
from .remote import BASE_API
from cosmicds import load_custom_vue_components
from cosmicds.utils import get_session_id
from cosmicds.components.login import Login
from cosmicds.components.speech_settings import SpeechSettings
from cosmicds.logger import setup_logger

filterwarnings(action="ignore", category=UserWarning)

if "AWS_EBS_URL" in os.environ:
    settings.main.base_url = os.environ["AWS_EBS_URL"]

logger = setup_logger("LAYOUT")


@solara.component
def BaseLayout(
    local_state: Optional[Reactive[BaseLocalState]] = None,
    children: list = [],
    story_name: str = "",
    story_title: str = "Cosmic Data Story",
):
    route_current, routes_current_level = solara.use_route()
    route_index = routes_current_level.index(route_current)

    selected_link = solara.use_reactive(route_index)
    def on_selected_link_change(new, old):
        logger.info(f"Selected link changed from {old} to {new}")
    selected_link.subscribe_change(on_selected_link_change)

    active = solara.use_reactive(False)
    class_code = solara.use_reactive("")
    update_db = solara.use_reactive(False)
    debug_mode = solara.use_reactive(True)

    debug_menu = solara.use_reactive(False)
    speech_menu = solara.use_reactive(False)

    def _component_setup():
        # Custom vue-only components have to be registered in the Page element
        #  currently, otherwise they will not be available in the front-end
        logger.info("Loaded custom vue files.")
        load_custom_vue_components()

    solara.use_memo(_component_setup)

    # Attempt to load saved setup state
    def _load_from_cache():
        cache = solara.cache.storage.get(f"cds-login-options-{get_session_id()}")

        if cache is not None:
            for key, state in [
                ("class_code", class_code),
                ("update_db", update_db),
                ("debug_mode", debug_mode),
            ]:
                if key in cache:
                    state.set(cache[key])

    solara.use_memo(_load_from_cache)

    if bool(auth.user.value):
        if BASE_API.user_exists:
            BASE_API.load_user_info(story_name, GLOBAL_STATE)
        elif bool(class_code.value):
            BASE_API.create_new_user(story_name, class_code.value, GLOBAL_STATE)
        else:
            logger.error("User is authenticated, but does not exist.")
            solara.use_router().push(auth.get_logout_url())
    else:
        logger.info("User has not authenticated.")
        BASE_API.clear_user(GLOBAL_STATE)

        login_dialog = Login(active, class_code, update_db, debug_mode)
        active.set(True)
        return

    # Just for testing
    # Ref(GLOBAL_STATE.fields.student.id).set(0)
    # Ref(GLOBAL_STATE.fields.classroom.class_info).set({"id": 0})
    # Ref(GLOBAL_STATE.fields.classroom.size).set(0)
    
    speech = Ref(GLOBAL_STATE.fields.speech)

    @solara.lab.computed
    def display_info():
        info = (auth.user.value or {}).get("userinfo")

        if info is not None and 'cds/name' in info and 'cds/email' in info:
            return {**info, "id": GLOBAL_STATE.value.student.id}

        return {
            "cds/name": "Undefined",
            "cds/email": "ERROR: No user",
            "id": "",
        }

    with solara.Column(style={"height": "100vh"}) as main:
        with rv.AppBar(elevate_on_scroll=False, app=True, flat=True, class_="cosmicds-appbar"):
            
            rv.Html(tag="h2", children=[f"{story_title}"])
            rv.Html(tag="h3", children=['Cosmic Data Stories'], class_="ml-4 app-title")

            rv.Spacer()

            with rv.Menu(
                v_model=debug_menu.value,
                offset_y=True,
                close_on_content_click=False,
                v_slots=[
                    {
                        "name": "activator",
                        "variable": "menu",
                        "children": rv.Btn(
                            v_on="menu.on",
                            icon=True,
                            children=[rv.Icon(children=["mdi-bug"])],
                            class_="hide-in-demo"
                        ),
                    }
                ],
            ):
                with rv.Card(width=250):
                    with rv.CardText():
                        rv.TextField(
                            value=f"{version('cosmicds')}",
                            label="CosmicDS Version",
                            readonly=True,
                            outlined=True,
                            dense=True,
                        )
                        try:
                            rv.TextField(
                                value=f"{version('hubbleds')}",
                                label="HubbleDS Version",
                                readonly=True,
                                outlined=True,
                                dense=True,
                            )
                        except PackageNotFoundError:
                            pass
                        rv.TextField(
                            value=f"{GLOBAL_STATE.value.student.id}",
                            label="Student ID",
                            readonly=True,
                            outlined=True,
                            dense=True,
                        )
                        rv.TextField(
                            value=f"{BASE_API.hashed_user}",
                            label="Student Hash",
                            readonly=True,
                            outlined=True,
                            dense=True,
                        )

            with rv.Menu(
                v_model=speech_menu.value,
                offset_y=True,
                close_on_content_click=False,
                v_slots=[
                    {
                        "name": "activator",
                        "variable": "menu",
                        "children": rv.Btn(
                            v_on="menu.on",
                            icon=True,
                            children=[rv.Icon(children=["mdi-tune-vertical"])]
                        ),
                    }
                ]
            ):
                initial_settings = GLOBAL_STATE.value.speech.model_dump()
                def update_speech_property(prop, value):
                    settings = speech.value.model_copy()
                    setattr(settings, prop, value)
                    speech.set(settings)
                SpeechSettings(
                    initial_state=initial_settings,
                    event_autoread_changed=lambda read: update_speech_property("autoread", read),
                    event_pitch_changed=lambda pitch: update_speech_property("pitch", pitch),
                    event_rate_changed=lambda rate: update_speech_property("rate", rate),
                    event_voice_changed=lambda voice: update_speech_property("voice", voice),
                )

            solara.lab.ThemeToggle(
                on_icon="mdi-brightness-4",
                off_icon="mdi-brightness-4",
                enable_auto=False,
            )

            with rv.Chip(class_="ma-2 piggy-chip"):                    
                if local_state:
                    # check that this doesn't make solara render the whole app. if it does, move the chip into its own component.
                    solara.Text(f"{local_state.value.piggybank_total} Points")

                rv.Icon(class_="ml-2",
                    children=["mdi-piggy-bank"],
                    color="var(--success-dark)")

        with rv.NavigationDrawer(
            app=True,
        ):
            with rv.ListItem():
                with rv.ListItemContent():
                    # We access the modified token information first, if that 
                    #  does not exist, we fall back to the default parameters 
                    #  returned by the `display_info` property
                    rv.ListItemTitle(
                        class_="text-h6", children=[f"{display_info.value['cds/name']}"]
                    )
                    rv.ListItemSubtitle(children=[f"{display_info.value['cds/email']}"])

                with rv.ListItemAction():
                    with rv.Btn(href=auth.get_logout_url(), icon=True):
                        rv.Icon(children=["mdi-logout"])

            rv.Divider()

            with rv.List(nav=True):
                with rv.ListItemGroup(
                    v_model=selected_link.value,
                ):
                    for i, route in enumerate(routes_current_level):
                        disabled = False
                        if (local_state is not None):
                            disabled = (
                                local_state.value.max_route_index is not None 
                                and i > local_state.value.max_route_index
                                )
                        with solara.Link(solara.resolve_path(route) if not disabled else solara.resolve_path(route_current.path)):
                            with rv.ListItem(disabled=disabled, inactive=disabled):
                                with rv.ListItemIcon():
                                    rv.Icon(children=f"mdi-numeric-{i}-circle")

                                with rv.ListItemContent():
                                    rv.ListItemTitle(
                                        children=f"{route.label if route.path != '/' else 'Introduction'}"
                                    )

        with rv.Content(class_="solara-content-main", style_="height: 100%"):
            with rv.Container(
                # children=children,
                class_="solara-container-main",
                style_="height: 100%; width: 100%; overflow: auto;",
                fluid=True,
            ):
                rv.Container(
                    children=children, style_="height: 100%; width: 100%", fluid=False
                )

        with rv.Footer(
            class_="text-center align-items",
            padless=True,
            app=True,
            inset=True,
        ):
            with rv.Card(
                flat=True, tile=True, class_="cosmicds-footer", style_="width: 100%;"
            ):
                rv.Divider()

                with solara.Columns([2, 10]):
                    with solara.Column(classes=["cosmicds-footer"]):
                        with rv.CardText():
                            solara.HTML(
                                unsafe_innerHTML=rf"""
                                {datetime.date.today().year} - <b>CosmicDS</b>
                                """,
                                style="font-size: 18px;",
                            )

                    with solara.Column(classes=["cosmicds-footer"]):
                        with rv.CardText():
                            solara.HTML(
                                tag="span",
                                unsafe_innerHTML="""
                            The material contained on this website is based upon 
                            work supported by NASA under award No. 80NSSC21M0002. 
                            Any opinions, findings, and conclusions or 
                            recommendations expressed in this material are those of 
                            the author(s) and do not necessarily reflect the views 
                            of the National Aeronautics and Space Administration.
                            """,
                                style="font-size: 12px; line-height: 12px",
                            )
