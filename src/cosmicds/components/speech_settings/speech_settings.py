import solara
from typing import Optional, Callable


@solara.component_vue("SpeechSettings.vue")
def SpeechSettings(
    initial_state: dict,
    event_autoread_changed: Optional[Callable[[bool], None]] = None,
    event_pitch_changed: Optional[Callable[[float], None]] = None,
    event_rate_changed: Optional[Callable[[float], None]] = None,
    event_voice_changed: Optional[Callable[[str], None]] = None,
):
    pass
