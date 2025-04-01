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
from reacton import ipyvue


from .state import GLOBAL_STATE, BaseLocalState, Speech
from .remote import BASE_API
from .components.breakpoint_watcher.breakpoint_watcher import BreakpointWatcher
from cosmicds import load_custom_vue_components
from cosmicds.utils import get_session_id
from cosmicds.components.login import Login
from cosmicds.components.speech_settings import SpeechSettings
from .components.theme_toggle import ThemeToggle
from cosmicds.components.tooltip_menu import TooltipMenu
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
    force_demo: bool = False,
):
    router = solara.use_router()
    route_current, routes_current_level = solara.use_route(peek=True)
    route_index = routes_current_level.index(route_current)

    selected_link = solara.use_reactive(route_index)
    stu_info_panel = solara.use_reactive([0])

    def on_selected_link_change(new, old):
        logger.info(f"Selected link changed from {old} to {new}")

    selected_link.subscribe_change(on_selected_link_change)

    active = solara.use_reactive(False)
    class_code = solara.use_reactive("")
    update_db = solara.use_reactive(False)
    debug_mode = solara.use_reactive(True)

    debug_menu = solara.use_reactive(False)
    speech_menu = solara.use_reactive(False)

    # Set up a watcher for vue break_point events
    break_point = solara.use_reactive("")
    BreakpointWatcher(
        event_set_breakpoint_info=lambda event: break_point.set(event["breakpoint"])
    )

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

    if force_demo:
        logger.info("Loading app in demo mode.")
        auth.user.set(
            {
                "userinfo": {
                    "cds/name": "Demo User",
                    "cds/email": "cosmicds@cfa.harvard.edu",
                    "cds/picture": "https://s.gravatar.com/avatar/d49c4a758d6e45538cd0fb4cd09e91eb?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fco.png",
                    "nickname": "cosmicds",
                    "name": "Demo User",
                    "picture": "https://s.gravatar.com/avatar/d49c4a758d6e45538cd0fb4cd09e91eb?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fco.png",
                    "updated_at": "2025-02-06T17:47:34.507Z",
                    "email": "cosmicds@cfa.harvard.edu",
                    "email_verified": True,
                }
            }
        )
        class_code.set("215")

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

        if info is not None and "cds/name" in info and "cds/email" in info:
            return {**info, "id": GLOBAL_STATE.value.student.id}

        return {
            "cds/name": "Undefined",
            "cds/email": "ERROR: No user",
            "id": "",
        }

    drawer = solara.use_reactive(None)

    with rv.AppBar(
        elevate_on_scroll=False,
        app=True,
        flat=True,
        clipped_left=True,
        class_="cosmicds-appbar",
    ):
        nav_icon = rv.AppBarNavIcon(v_on="tooltip.on")
        ipyvue.use_event(nav_icon, "click", lambda *args: drawer.set(not drawer.value))

        rv.Tooltip(
            bottom=True,
            v_slots=[
                {
                    "name": "activator",
                    "variable": "tooltip",
                    "children": [
                        nav_icon,
                    ],
                }
            ],
            children=["Close Navigation" if drawer.value else "Open Navigation"],
        )

        rv.Html(tag="h2", children=["Hubble's Law"], class_="pl-5")
        # rv.Html(
        #     tag="h4",
        #     children=["Cosmic Data Story"],
        #     class_="ml-8 app-title",
        # )

        rv.Spacer()

        with rv.Chip(class_="ma-2 piggy-chip"):

            if local_state is not None:
                # TODO: Check that this doesn't make solara render the whole
                #  app. if it does, move the chip into its own component.
                solara.Text(f"{local_state.value.piggybank_total} Points")

            rv.Icon(
                class_="ml-2",
                children=["mdi-piggy-bank"],
                color="var(--success-dark)",
            )

        rv.Divider(vertical=True, class_="mx-2")

        with TooltipMenu(
            v_model=speech_menu.value,
            icon="mdi-tune-vertical",
            tooltip="Speech Settings",
            bottom=True,
            offset_y=True,
            close_on_content_click=False,
        ):
            initial_settings = GLOBAL_STATE.value.speech.model_dump()

            def update_speech_property(prop, value):
                settings = speech.value.model_copy()
                setattr(settings, prop, value)
                speech.set(settings)

            SpeechSettings(
                initial_state=initial_settings,
                event_autoread_changed=lambda read: update_speech_property(
                    "autoread", read
                ),
                event_pitch_changed=lambda pitch: update_speech_property(
                    "pitch", pitch
                ),
                event_rate_changed=lambda rate: update_speech_property("rate", rate),
                event_voice_changed=lambda voice: update_speech_property(
                    "voice", voice
                ),
            )

        ThemeToggle(
            on_icon="mdi-brightness-4",  # dark mode icon
            off_icon="mdi-brightness-4",  # light mode icon
            enable_auto=False,
            default_theme="dark",
            enforce_default=True,
        )

    with rv.NavigationDrawer(
        v_model=drawer.value,
        on_v_model=drawer.set,
        app=True,
        clipped=True,
        v_slots=[
            {
                "name": "append",
                "variable": "btm",
                "children": [
                    rv.ExpansionPanels(
                        v_model=stu_info_panel.value,
                        on_v_model=stu_info_panel.set,
                        flat=True,
                        tile=True,
                        style_="padding-right: 1px;",
                        children=[
                            rv.ExpansionPanel(
                                class_="pa-0 ma-0",
                                children=[
                                    rv.ExpansionPanelHeader(
                                        class_="mx-2 my-0",
                                        children=[
                                            rv.Row(
                                                class_="flex align-center",
                                                children=[
                                                    rv.Icon(
                                                        children="mdi-account",
                                                        class_="mr-4",
                                                    ),
                                                    rv.Html(
                                                        tag="h4",
                                                        children="Student Info",
                                                    ),
                                                ],
                                            )
                                        ],
                                    ),
                                    rv.ExpansionPanelContent(
                                        children=[
                                            rv.TextField(
                                                value=f"{display_info.value['cds/email']}",
                                                label="Email",
                                                readonly=True,
                                                outlined=True,
                                                dense=True,
                                            ),
                                            rv.TextField(
                                                value=f"{GLOBAL_STATE.value.student.id}",
                                                label="Student ID No.",
                                                readonly=True,
                                                outlined=True,
                                                dense=True,
                                            ),
                                            rv.TextField(
                                                value=f"{BASE_API.hashed_user}",
                                                label="Anonymized ID",
                                                readonly=True,
                                                outlined=True,
                                                dense=True,
                                                hide_details=True,
                                            ),
                                        ]
                                    ),
                                ],
                            )
                        ],
                    )
                ],
            }
        ],
    ) as navigation_drawer:
        with rv.List(
            nav=True,
        ):
            if break_point.value in ["xs", "sm", "md"]:
                with rv.Row(class_="flex justify-end pb-2 ml-0"):
                    solara.IconButton(
                        "mdi-close",
                        on_click=lambda: drawer.set(False),
                        right=True,
                        x_small=True,
                    )

            with rv.ListItemGroup(
                v_model=selected_link.value,
            ):

                def _change_local_url(path, location):
                    if path != "/":
                        router.push(f"{router.root_path}{path}")
                    else:
                        location.pathname = settings.main.base_url

                for i, route in enumerate(routes_current_level):
                    disabled = False
                    if local_state is not None:
                        disabled = (
                            local_state.value.max_route_index is not None
                            and i > local_state.value.max_route_index
                        )

                    with rv.ListItem(
                        disabled=disabled,
                        inactive=disabled,
                        link=True,
                    ) as list_item:
                        with rv.ListItemIcon(class_="mr-4"):
                            rv.Icon(children=f"mdi-numeric-{i}-circle")

                        with rv.ListItemContent(
                            style_="white-space: normal; overflow: visible; text-overflow: clip;",
                            class_="px-0 mx-0",
                        ):
                            rv.ListItemTitle(
                                children=f"{route.label if route.path != '/' else 'Introduction'}"
                            )

                    solara.v.use_event(
                        list_item,
                        "click",
                        lambda *args, path=solara.resolve_path(
                            route
                        ), location=solara.use_context(
                            solara.routing._location_context
                        ): _change_local_url(
                            path, location
                        ),
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
