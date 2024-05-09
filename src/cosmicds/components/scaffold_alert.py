import solara
import inspect


def ScaffoldAlert(
    vue_path: str,
    event_back_callback=lambda *args: True,
    event_next_callback=lambda *args: True,
    show=False,
    can_advance=False,
    hide_next=False,
    fr_observer=None,
    free_responses=[],
    disable_next=False,
    fr_listener=None,
    state_view=None,
    event_force_transition=lambda *args: None,
    **kwargs
):
    if not show:
        return

    def _ScaffoldAlert(
        event_back_callback,
        event_next_callback,
        can_advance,
        hide_next,
        frObserver,
        freeResponses,
        disableNext,
        frListener,
        state_view,
        event_force_transition,
    ):
        pass

    signature = inspect.signature(_ScaffoldAlert)
    parameters = list(signature.parameters.values()) + [
        inspect.Parameter(
            name=k,
            kind=inspect.Parameter.KEYWORD_ONLY,
        )
        for k in kwargs.keys()
    ]
    _ScaffoldAlert.__signature__ = signature.replace(parameters=parameters)

    _ScaffoldAlert = solara.component_vue(vue_path)(_ScaffoldAlert)

    return _ScaffoldAlert(
        event_back_callback=event_back_callback,
        event_next_callback=event_next_callback,
        can_advance=can_advance,
        hide_next=hide_next,
        frObserver=fr_observer,
        freeResponses=free_responses,
        disableNext=disable_next,
        frListener=fr_listener,
        state_view=state_view,
        event_force_transition=event_force_transition,
        **kwargs
    )
