from pathlib import Path

import ipyvuetify as v
import solara
from reacton import ipyvuetify as rv

import datetime
from solara_enterprise import auth


@solara.component
def Layout(children=[]):
    level = solara.use_route_level()  # returns 0
    route_current, routes_current_level = solara.use_route()
    selected_link, on_selected_link = solara.use_state(0)

    with rv.App(style_="height: 100vh") as main:
        # with rv.Html(tag="div", style_="height: 100vh") as main:
        solara.Title("Cosmic Data Stories")

        with rv.AppBar(elevate_on_scroll=False, app=True, flat=True):
            rv.ToolbarTitle(children=["CosmicDS"])

            rv.Spacer()

            with rv.Btn(icon=True):
                rv.Icon(children=["mdi-tune-vertical"])

            with rv.Btn(icon=True):
                rv.Icon(children=["mdi-brightness-4"])

            with rv.Chip(class_="ma-2"):
                with rv.Avatar(left=True, class_="darken-4"):
                    solara.Text("1")

                solara.Text("Points")

        with rv.NavigationDrawer(app=True):  # , width=300):
            with rv.ListItem():
                with rv.ListItemContent():
                    rv.ListItemTitle(class_="text-h6", children=["Nicholas Earl"])
                    rv.ListItemSubtitle(children=["Epsilon Class"])

            rv.Divider()

            with rv.List(nav=True):
                with rv.ListItemGroup(
                    v_model=selected_link, on_v_model=on_selected_link
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
            class_="text-center",
            padless=True,
            app=True,
            inset=True,
        ):
            with rv.Card(flat=True, tile=True, style_="width: 100%"):
                rv.Divider()

                with rv.CardText():
                    solara.HTML(
                        tag="span",
                        unsafe_innerHTML=rf"""
                    The material contained on this website is based upon 
                    work supported by NASA under award No. 80NSSC21M0002. 
                    Any opinions, findings, and conclusions or 
                    recommendations expressed in this material are those of 
                    the author(s) and do not necessarily reflect the views 
                    of the National Aeronautics and Space Administration.
                    <br />{datetime.date.today().year} - <strong>CosmicDS</strong>
                    """,
                    )

    return main
