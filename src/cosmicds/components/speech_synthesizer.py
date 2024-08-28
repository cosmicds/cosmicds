import os
import solara

@solara.component_vue(os.path.join("..", "vue_components", "SpeechSynthesizer.vue"))
def SpeechSynthesizer(
    autoread: bool,
    voice: str,
    pitch: float,
    rate: float,
):
    pass
