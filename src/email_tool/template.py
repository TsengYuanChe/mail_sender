from pathlib import Path


def load_template(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def render_template(template: str, name: str) -> str:
    return template.replace("{{ name }}", name)