from typing import Callable

import solara


@solara.component_vue("BreakpointWatcher.vue")
def BreakpointWatcher(
    event_set_breakpoint_info: Callable[[dict], None] = None,
):
    pass
