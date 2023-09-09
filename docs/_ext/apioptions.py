from __future__ import annotations

from docutils.statemachine import StringList
from sphinx.ext.autodoc import ClassDocumenter


class ApiOptionsDocumenter(ClassDocumenter):
    objtype = "apioptions"
    directivetype = "attribute"
    member_order = 60

    # must be higher than ClassDocumenter
    priority = 16

    def add_directive_header(self, sig):
        pass

    def add_content(self, more_content: StringList | None) -> None:
        self.add_line(", ".join([f"``{i}``" for i in self.object]), self.get_sourcename())


def setup(app):
    app.setup_extension("sphinx.ext.autodoc")
    app.add_autodocumenter(ApiOptionsDocumenter)
