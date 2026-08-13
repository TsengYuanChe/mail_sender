from email_tool.template import load_template, render_template


def test_load_template(tmp_path):
    template_file = tmp_path / "template.html"
    template_file.write_text(
        "<p>Hello</p>",
        encoding="utf-8",
    )

    result = load_template(str(template_file))

    assert result == "<p>Hello</p>"


def test_render_template():
    template = "<p>Hi {{ name }},</p>"

    result = render_template(template, "Adam")

    assert result == "<p>Hi Adam,</p>"