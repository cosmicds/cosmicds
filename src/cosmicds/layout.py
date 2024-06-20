import datetime
import os
from warnings import filterwarnings

import solara
from solara.alias import rv
from solara.lab import theme as theme
from solara.server import settings
from solara_enterprise import auth

filterwarnings(action="ignore", category=UserWarning)

if "AWS_EBS_URL" in os.environ:
    settings.main.base_url = os.environ["AWS_EBS_URL"]

active = solara.reactive(False)
user_info = solara.reactive({})
class_code = solara.reactive("")
update_db = solara.reactive(False)
debug_mode = solara.reactive(False)


def get_session_id() -> str:
    """Returns the session id, which is stored using a browser cookie."""
    import solara.server.kernel_context

    context = solara.server.kernel_context.get_current_context()
    return context.session_id


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


def _save_to_cache():
    solara.cache.storage[f"cds-login-options-{get_session_id()}"] = {
        "class_code": class_code.value,
        "update_db": update_db.value,
        "debug_mode": debug_mode.value,
    }


@solara.component
def Login(**btn_kwargs):
    with rv.Dialog(
        v_model=active.value,
        on_v_model=active.set,
        max_width=600,
        # fullscreen=True,
        persistent=True,
        overlay_color="grey darken-2",
    ) as login:
        with rv.Card():
            with rv.CardText():
                with rv.Container(
                    class_="d-flex align-center flex-column justify-center"
                ):
                    solara.Image(
                        "/static/public/cosmicds_logo_transparent_for_dark_backgrounds.png"
                    )
                    solara.Text(
                        "Hubble's Law Data Story", classes=["display-1", "py-12"]
                    )

                    solara.InputText(
                        label="Class Code", value=class_code, continuous_update=True
                    )

                    # TODO: hide these in production
                    with solara.Row():
                        solara.Checkbox(label="Update DB", value=update_db)
                        solara.Checkbox(label="Debug Mode", value=debug_mode)

                    solara.Button(
                        "Sign in",
                        href=auth.get_login_url(),
                        disabled=not class_code.value,
                        outlined=False,
                        large=True,
                        color="success",
                        on_click=_save_to_cache,
                    )

    return login


selected_link = solara.reactive(0)


@solara.component
def BaseLayout(
    children=[], global_state=None, story_name=None, story_title="Cosmic Data Story"
):
    solara.Title(f"{story_title}")

    route_current, routes_current_level = solara.use_route()

    # def _setup_user():
    #     _load_from_cache()
    #     global_state._setup_user(story_name, class_code.value)
    #
    # solara.use_memo(_setup_user)

    @solara.lab.computed
    def display_info():
        info = (auth.user.value or {}).get("userinfo")

        if info is not None:
            return info

        return {
            "name": "Undefined",
            "email": "ERROR: No user",
            "id": global_state.student.id.value,
        }

    with solara.Column(style={"height": "100vh"}) as main:
        if not bool(auth.user.value):
            global_state._clear_user()

            # Attempt to load saved setup state
            _load_from_cache()

            login_dialog = Login()
            active.set(True)
            return main
        else:
            _load_from_cache()
            global_state._setup_user(story_name, class_code.value)

        with rv.AppBar(elevate_on_scroll=False, app=True, flat=True):
            rv.ToolbarTitle(children=[f"{story_title}"])

            rv.Spacer()

            with rv.Btn(icon=True):
                rv.Icon(children=["mdi-tune-vertical"])

            solara.lab.ThemeToggle(
                on_icon="mdi-brightness-4",
                off_icon="mdi-brightness-4",
                enable_auto=False,
            )

            with rv.Chip(class_="ma-2"):
                with rv.Avatar(left=True, class_="darken-4"):
                    solara.Text("1")

                solara.Text("Points")

        with rv.NavigationDrawer(app=True):  # , width=300):
            with rv.ListItem():
                with rv.ListItemContent():
                    rv.ListItemTitle(
                        class_="text-h6", children=[f"{display_info.value['name']}"]
                    )
                    rv.ListItemSubtitle(children=[f"{display_info.value['email']}"])

                with rv.ListItemAction():
                    with rv.Btn(href=auth.get_logout_url(), icon=True):
                        rv.Icon(children=["mdi-logout"])

            rv.Divider()

            with rv.List(nav=True):
                with rv.ListItemGroup(
                    v_model=selected_link.value,
                    on_v_model=lambda v: selected_link.set(v),
                ):
                    for i, route in enumerate(routes_current_level):
                        with solara.Link(solara.resolve_path(route)):
                            with rv.ListItem():
                                with rv.ListItemIcon():
                                    rv.Icon(children="mdi-view-dashboard")

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

    return main
