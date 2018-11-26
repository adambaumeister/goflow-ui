from flask import render_template
class Page:
    """
    Object for rendering a Page using Flask
    Supports wrappers such as headers, footers, head, etc.
    :param header_template (str)(Optional): Header template to add to page
    :param footer_template (str)(Optional): Footer template to add to page
    :param body_template (str)(Optional): Body template for page
    """
    def __init__(self, header_template='', footer_template='', body_template=''):
        self.header_template = header_template
        self.footer_template = footer_template
        self.body_template = body_template

    def render_header(self, **kwargs):
        return render_template(self.header_template, **kwargs)

    def render_body(self, **kwargs):
        return render_template(self.body_template, **kwargs)

    def render_footer(self, **kwargs):
        return render_template(self.footer_template, **kwargs)

    def render_page(self, **kwargs):
        header = self.render_header(**kwargs)
        body = self.render_body(**kwargs)
        footer = self.render_footer(**kwargs)
        return header + body + footer

