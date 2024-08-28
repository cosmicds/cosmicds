import os
import solara
from typing import Optional


@solara.component_vue(os.path.join("..", "vue_components", "SpeechSynthesizer.vue"))
def SpeechSynthesizer(
    options: Optional[dict] = None,
):
    pass
