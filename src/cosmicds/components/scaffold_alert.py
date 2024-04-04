import solara


def ScaffoldAlert(
    vue_path: str,
    event_back_callback=lambda *args: True,
    event_next_callback=lambda *args: True,
    show=False,
    can_advance=False,
    fr_observer=None,
    free_responses=[],
    disable_next=False,
    fr_listener=None,
    state_view=None,
    event_force_transition=lambda *args: None,
):
    if not show:
        return

    @solara.component_vue(vue_path)
    def _ScaffoldAlert(
        event_back_callback,
        event_next_callback,
        can_advance,
        frObserver,
        freeResponses,
        disableNext,
        frListener,
        state_view,
        event_force_transition,
    ):
        pass

    return _ScaffoldAlert(
        event_back_callback=event_back_callback,
        event_next_callback=event_next_callback,
        can_advance=can_advance,
        frObserver=fr_observer,
        freeResponses=free_responses,
        disableNext=disable_next,
        frListener=fr_listener,
        state_view=state_view,
        event_force_transition=event_force_transition,
    )
