from jinja2 import Environment, PackageLoader


def render_template(template):
    env = Environment(loader=PackageLoader('monitoring', 'templates'))
    template = env.get_template(template)
    return str(template.render())

