import solara


def ScaffoldAlert(
    vue_path: str,
    event_back_callback=lambda: False,
    event_next_callback=lambda: False,
    show=False,
    can_advance=False,
    frObserver=None,
    freeResponses=[],
    disableNext=False,
    frListener=None,
    state_view=None,
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
    ):
        pass

    return _ScaffoldAlert(
        event_back_callback=event_back_callback,
        event_next_callback=event_next_callback,
        can_advance=can_advance,
        frObserver=frObserver,
        freeResponses=freeResponses,
        disableNext=disableNext,
        frListener=frListener,
        state_view=state_view,
    )
