import solara
import inspect

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
    **kwargs
):
    """
        This works indirectly with the ScaffoldAlert.vue component. (We load the vue file for each specific guideline, which in turn uses the ScaffoldAlert.vue component as a template.)

        vue_path: str,
            vue file for the guideline
        event_back_callback=lambda *args: True,
            function you want the guideline to call when user clicks "back"
        event_next_callback=lambda *args: True, 
            function you want the guideline to call when user clicks "next"
        show=False,
            Have the conditions needed to display this guideline been met? (Generally, "are you at the correct marker?")
        can_advance=False,
            - Have the conditions to advance to next guideline been met (i.e. have you unlocked the gate guarding the next guideline)? 
            - If False, display whatever is in the before-next template in place of the "next" button. 
            - If True, display "next" button (or whatever text you specified for the button in "nextText" instead of "next.")
            - If you don't want to display a next button at all, you can set this to False and leave the before-next template blank. 

        fr_observer=None,
            ? TBD depending on how we connect this to the state. (The original usage of this in the voila version was to observe if new free response boxes were being added as the student progressed through the guideline, as in the case of the multi-step, expanding guidelines).
        free_responses=[],
            ? TBD depending on how we connect this to the state. (Could be a list of tags to assign to each free response entry).
        disable_next=False,
            Next button is disabled until free response questions have been answered. (Note to team - are there other cases where we disable the button?)
        fr_listener=None,
            ? TBD depending on how we connect this to the state. (The original usage of this in the voila version was to vet whether students had entered content into the box that passed the relevant validation checks).
        state_view=None,
            State components you want to pass to the guideline vue component. (Note that the vue component cannot change the state components directly. They should always be changed on the python side by a callback function.)
        event_force_transition=lambda *args: None,
            We don't use this anywhere yet, so update this as needed, but we could use this to specify a callback that transitions to somewhere other than the next/previous marker.
        **kwargs
    """
    if not show:
        return

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
        frObserver=fr_observer,
        freeResponses=free_responses,
        disableNext=disable_next,
        frListener=fr_listener,
        state_view=state_view,
        event_force_transition=event_force_transition,
        **kwargs
    )
