import solara


@solara.component_vue("LocationHelper.vue")
def LocationHelper(url: str):
    """
    Forcibly sets the window location to the given url on instantiation.

    Parameters
    ----------
    url : str
        The absolute url to which the window location should be set.
    """
    pass
