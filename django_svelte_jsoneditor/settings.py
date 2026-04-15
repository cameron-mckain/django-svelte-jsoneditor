from django.conf import settings


DEFAULT_SVELTE_JSONEDITOR_PROPS = {
    "mode": "tree",
    "mainMenuBar": True,
    "navigationBar": True,
    "statusBar": True,
    "askToFormat": True,
    "readOnly": False,
    "indentation": 4,
    "tabSize": 4,
    "escapeControlCharacters": False,
    "escapeUnicodeCharacters": False,
    "flattenColumns": True,
}


def check_props(props):
    """Accept props without validation — svelte-jsoneditor validates on the JS side,
    and hard-gating here blocks consumers from passing new props added upstream."""
    return props


def get_props():
    """Get default props overridden by any props set in the SVELTE_JSONEDITOR_PROPS setting"""
    return check_props(
        {
            **DEFAULT_SVELTE_JSONEDITOR_PROPS,
            **getattr(settings, "SVELTE_JSONEDITOR_PROPS", {}),
        }
    )
