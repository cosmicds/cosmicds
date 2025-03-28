import solara

@solara.component_vue("tooltip_menu.vue")
def TooltipMenuVue(
    icon = 'mdi-menu',
    tooltip = '',
    children = [],
    top = False,
    bottom = False,
    left = False,
    right = False,
    offset_x = False,
    offset_y = False,
    attach = False,
    close_on_content_click = True,
    close_on_click = True,
    open_on_click = True,
    open_on_hover = False,
    open_on_focus = False,
    **kwargs
):
    pass