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
        self.nav_buttons = []

    def render_header(self, **kwargs):
        return render_template(self.header_template, **kwargs, nav_buttons=self.nav_buttons)

    def render_body(self, **kwargs):
        return render_template(self.body_template, **kwargs)

    def render_footer(self, **kwargs):
        return render_template(self.footer_template, **kwargs)

    def add_nav_button(self, href, name):
        nav = NavButton(href, name)
        self.nav_buttons.append(nav)

    def render_page(self, **kwargs):
        header = self.render_header(**kwargs)
        body = self.render_body(**kwargs)
        footer = self.render_footer(**kwargs)
        return header + body + footer

    def register_form(self):
        """
        Register_form

        Generates a Form object and returns it
        :return: empty Form
        """
        f = Form()
        return f

class NavButton:
    def __init__(self, href, name):
        self.href = href
        self.name = name


class Form:
    def __init__(self):
        """
        Form
        Used to parse POST and GET query arguments, do validation and other transformations.
        MAde up of a collection of Input objects.
        """
        self.inputs = {}

    def register_input(self, name, type):
        i = Input(name, type)
        self.inputs[name] = i
        return i

    def parse(self, form_args):
        """
        Parse
        Take form_args as args from Flask and parse them into Input objects
        :param form_args:
        :return:
        """
        for name, i in self.inputs.items():
            if name in form_args:
                self.inputs[name].validate(form_args[name])
            else:
                self.inputs[name].take_default()


        for name, value in form_args.items():
            self.inputs[name].validate(value)

class Input:
    def __init__(self, name, type="text"):
        self.validation_func = {
            "text": self.validate_text,
            "int": self.validate_int,
        }
        self.name = name
        self.type = type
        self.value = ''
        self.default = ''

    def validate(self, v):
        self.validation_func[self.type](v)

    def validate_text(self, v):
        self.value = v
        return True

    def validate_int(self, v):
        if int(v):
            self.value = v
            return True
        else:
            return False

    def take_default(self):
        self.value = self.default
