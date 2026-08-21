import re
from pathlib import Path

VARIABLE_PATTERN = re.compile(
    r"\{\{\s*(\w+)\s*\}\}"
)


def extract_template_variables(
    template: str,
) -> set[str]:
    return set(
        VARIABLE_PATTERN.findall(template)
    )

def load_template(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def render_template(
    template: str,
    variables: dict[str, str]
) -> str:
    result = template
    
    for key, value in variables.items():
        result = result.replace(
            "{{ " + key + " }}",
            value
        )
    
    return result