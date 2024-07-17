from solara import component_vue

@component_vue("InfoDialog.vue")
def InfoDialog(
    dialog: bool = False,
    title: str = "",
    content: str = "",
    hasImage: bool = True,
    image: str = "",
    altText: str = "",
):
    pass
