from email_tool.template import load_template, render_template, extract_template_variables


def test_load_template(tmp_path):
    template_file = tmp_path / "template.html"
    template_file.write_text(
        "<p>Hello</p>",
        encoding="utf-8",
    )

    result = load_template(str(template_file))

    assert result == "<p>Hello</p>"


def test_render_template():
    template = (
        "<p>Hi {{ name }},</p>"
        "<p>Company: {{ company }}</p>"
        "<p>Position: {{ position }}</p>"
    )

    result = render_template(
        template,
        {
            "name": "Adam",
            "company": "OpenAI",
            "position": "Engineer",
        },
    )

    assert result == (
        "<p>Hi Adam,</p>"
        "<p>Company: OpenAI</p>"
        "<p>Position: Engineer</p>"
    )
    
def test_extract_template_variables():
    template = (
        "<p>Hi {{ name }}</p>"
        "<p>Company: {{ company }}</p>"
        "<p>Email: {{ email }}</p>"
    )

    result = extract_template_variables(
        template
    )

    assert result == {
        "name",
        "company",
        "email",
    }


def test_extract_template_variables_with_spaces():
    template = (
        "{{name}} "
        "{{ company }} "
        "{{   position   }}"
    )

    result = extract_template_variables(
        template
    )

    assert result == {
        "name",
        "company",
        "position",
    }
