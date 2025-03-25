from typing import Callable, Optional, Literal
import warnings


import solara
from solara.lab import theme
from solara.server import settings
from solara.components.component_vue import component_vue

warnings.simplefilter('always', UserWarning)


@component_vue("theming.vue")
def _ThemeToggle(
    theme_dark: bool | None | str,
    event_sync_themes: Callable[[str], None],
    enable_auto: bool,
    on_icon: str,
    off_icon: str,
    auto_icon: str,
    clicks: int = 0,
    default_theme: Optional[str] = None,
    force_default: bool = False,
    disable: bool = False,
):
    pass

def theme_to_bool(theme: str | None) -> bool | None:
    """
    Convert a theme string to a boolean value.
    """
    if theme is None or theme == "auto":
        return None
    if theme.lower() == "dark":
        return True
    elif theme.lower() == "light":
        return False

    raise ValueError(f"Invalid theme value: {theme}. Must be 'dark', 'light', 'auto', or None.")


ThemesType = Literal["dark", "light", "auto", None]

def is_auto(theme: ThemesType) -> bool:
    """
    Check if the theme is set to auto.
    """
    return theme in ["auto", None]


@solara.component
def ThemeToggle(
    on_icon: str = "mdi-weather-night",
    off_icon: str = "mdi-weather-sunny",
    auto_icon: str = "mdi-brightness-auto",
    disable: bool = False,
    enable_auto: bool = True,
    default_theme: ThemesType  = None,
    default_to_server: bool = False,
    enforce_default: bool = False,
):
    """
    Insert a toggle switch for user to switch between light and dark themes.

    ```solara
    ThemeToggle(
        on_icon="mdi-weather-night",
        off_icon="mdi-brightness-7",
        enable_auto=True,
        default_theme=None,
        default_to_server=True,
        enforce_default=True,
    )
    ```

    ## Arguments
    - `on_icon`: The icon to display when the dark theme is enabled.
    - `off_icon`: The icon to display when the dark theme is disabled.
    - `auto_icon`: The icon to display when the theme is set to auto. Only visible if `enable_auto` is `True`.
    - `enable_auto`: Whether to enable the auto detection of dark mode.
    
    ### Default theme options:
    _We will *never* override what is in the user's local storage if they have already visited the site_
    - `default_theme` [None]: light, dark, auto (or None)
    - `default_to_server` [False]: Set's the default theme to whatever is set on `settings.theme.variant` which set by `--theme-variant` [default: light]
    - `enforce_default` [False]: When used with `enable_auto = True`, and has no local setting set, this will override prefers-color-scheme 
                         to use the theme set with `default_theme` (or the server theme if default_to_server=True).
    
    
    """

    def sync_themes(selected_theme: str):
        theme.dark = selected_theme
    
    warning_list = [] # keep the list for debugging purposes
    
    # Really shouldn't enable auto and request a default theme.
    # Unless enforece_default = True, we will just ignore the default_theme
    if enable_auto and not is_auto(default_theme):
        warning_list.append("default_theme will be ignored when enable_auto is True.")
        warnings.warn(warning_list[-1], UserWarning, stacklevel=2)
    
    # You really shouldn't set a default theme and ask to set it to the server theme
    # Just don't set the default_theme argument. 
    # For now we will overwrite what was passed to default_theme
    if not is_auto(default_theme) and default_theme != settings.theme.variant.value.lower()  and default_to_server:
        warning_list.append(f"""
                      default_theme ({default_theme}) and server defined theme ({settings.theme.variant.value.lower()}) disagree. 
                      With default_to_server set to true, the server theme will be used.
                      """)
        warnings.warn(warning_list[-1], UserWarning, stacklevel=2)

    if default_to_server:
        default_theme = settings.theme.variant.value
    
    # You've not set a desired theme, but want to *not* automatically detect it.
    # So instead I will detect it, but the user will not be able to toggle back to 'auto' mode.
    # This is solara's default behavior
    if enable_auto==False and is_auto(default_theme):
        warning_list.append(f"default_theme is {default_theme} and enable_auto is {enable_auto}. Defaulting to 'auto' because site should follow system settings.")
        warnings.warn(warning_list[-1], UserWarning, stacklevel=2)
    
    
    
    # Really this just means the developer wants to force an intial theme,
    # but allow the user to change it to 'auto' if they want. This is reasonable,
    # and should probably be default behavior, but I am warning about it because
    # it is not the default behavior of solara and "enable_auto" suggests that it will set it automatically
    if enforce_default and enable_auto:
        warning_list.append(f"""
                      `enforce_default` and `enable_auto` should not both be true. 
                      `enable_auto` is meant to allow the user's system 
                      settings set the default color scheme. However,
                      `enforce_default` will override this to the default_theme: {default_theme}.
                      """)
        warnings.warn(warning_list[-1], UserWarning, stacklevel=2)


    return _ThemeToggle(
        theme_dark=theme.dark,
        event_sync_themes=sync_themes,
        enable_auto=enable_auto,
        on_icon=on_icon,
        off_icon=off_icon,
        auto_icon=auto_icon,
        default_theme=default_theme,
        force_default=enforce_default,
        disable=disable,
    )
