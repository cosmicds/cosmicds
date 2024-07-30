import solara
import inspect
from pathlib import Path
from typing import Callable


def ScaffoldAlert(
    vue_path: str | Path,
    event_back_callback: Callable = lambda *args: True,
    event_next_callback: Callable = lambda *args: True,
    show: bool = False,
    can_advance: bool = False,
    scroll_on_mount: bool = True,
    fr_observer=None,
    free_responses: list = None,
    disable_next: bool = False,
    fr_listener=None,
    state_view: dict = None,
    event_force_transition: Callable = lambda *args: None,
    **kwargs
):
    """
    Initializes and configures a ScaffoldAlert component.

    This works indirectly with the ScaffoldAlert.vue component. (We load the
    vue file for each specific guideline, which in turn uses the
    `ScaffoldAlert.vue` component as a template.)

    Parameters
    ----------
    vue_path : str
        The path to the Vue component file.
    event_back_callback : callable, optional
        A callback function triggered when the "back" event occurs. Defaults
        to a lambda that always returns True.
    event_next_callback : callable, optional
        A callback function triggered when the "next" event occurs. Defaults
        to a lambda that always returns True.
    show : bool, optional
        Flag to determine if the alert is visible. Have the conditions needed
        to display this guideline been met? (Generally, "are you at the
        correct marker?".) Defaults to False.
    can_advance : bool, optional
        Flag to determine if advancing to the next step is allowed. Defaults
        to False.

        - Have the conditions to advance to next guideline been met (i.e. have
        you unlocked the gate guarding the next guideline)?
        - If False, display whatever is in the before-next template in place
        of the "next" button.
        - If True, display "next" button (or whatever text you specified for
        the button in "nextText" instead of "next.")
        - If you don't want to display a next button at all, you can set this
        to False and leave the before-next template blank.
    scroll_on_mount: bool, optional
        Flag to determine whether or not the browser view will scroll to
        the guideline when it is mounted. Defaults to True.
    fr_observer : object, optional
        An observer for free response events. TBD depending on how we connect
        this to the state. (The original usage of this in the Voila version
        was to observe if new free response boxes were being added as the
        student progressed through the guideline, as in the case of the
        multistep, expanding guidelines). Defaults to None.
    free_responses : list, optional
        A list of free response items. TBD depending on how we connect this to
        the state. (Could be a list of tags to assign to each free response
        entry). Defaults to an empty list.
    disable_next : bool, optional
        Flag to disable the "next" button. Next button is disabled until free
        response questions have been answered. (Note to team - are there other
        cases where we disable the button?) Defaults to False.
    fr_listener : callable, optional
        A listener for free response events. TBD depending on how we connect
        this to the state. (The original usage of this in the Voila version
        was to vet whether students had entered content into the box that
        passed the relevant validation checks). Defaults to None.
    state_view : dict, optional
        The state view object for managing component state. (Note that the vue
        component cannot change the state components directly. They should
        always be changed on the python side by a callback function.)
        Defaults to None.
    event_force_transition : callable, optional
        A callback function to force a state transition. We don't use this
        anywhere yet, so update this as needed, but we could use this to
        specify a callback that transitions to somewhere other than the
        next/previous marker. Defaults to a lambda that does nothing.
    **kwargs
        Additional keyword arguments for further customization.

    Returns
    -------
    None
    """
    if not show:
        return

    def _ScaffoldAlert(
        event_back_callback,
        event_next_callback,
        can_advance,
        scroll_on_mount,
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
        scroll_on_mount=scroll_on_mount,
        frObserver=fr_observer,
        freeResponses=free_responses,
        disableNext=disable_next,
        frListener=fr_listener,
        state_view=state_view,
        event_force_transition=event_force_transition,
        **kwargs
    )
