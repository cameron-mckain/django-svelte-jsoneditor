import json
from django.forms import Textarea

from .settings import DEFAULT_SVELTE_JSONEDITOR_PROPS, check_props, get_props


class SvelteJSONEditorWidget(Textarea):
    template_name = "django_svelte_jsoneditor/widgets/svelte_jsoneditor.html"

    def __init__(self, props=None, attrs=None, wrapper_class="svelte-jsoneditor-wrapper", allow_file_import=False):
        if attrs is None:
            attrs = {}

        self.props = {} if props is None else props.copy()
        self.wrapper_class = wrapper_class
        self.allow_file_import = allow_file_import

        check_props(self.props)
        attrs.update({"class": "hidden"})

        super().__init__(attrs)

    def format_value(self, value):
        if value is None or value == "":
            return super().format_value(value)
        try:
            parsed = value if isinstance(value, (dict, list)) else json.loads(value)
        except (TypeError, ValueError):
            return super().format_value(value)
        merged = {**DEFAULT_SVELTE_JSONEDITOR_PROPS, **self.props}
        indent = merged.get("indentation") or 4
        return json.dumps(parsed, indent=indent, ensure_ascii=False)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"].update({"props": json.dumps({**get_props(), **self.props})})
        context["widget"].update({"wrapper_class": self.wrapper_class})
        context["widget"].update({"allow_file_import": self.allow_file_import})
        return context

    class Media:
        css = {"all": ("django_svelte_jsoneditor/css/svelte_jsoneditor.css",)}


class ReadOnlySvelteJSONEditorWidget(SvelteJSONEditorWidget):
    def __init__(self, attrs=None):
        props = {"mode": "view", "readOnly": True, "navigationBar": False}
        super().__init__(props=props, attrs=attrs)
