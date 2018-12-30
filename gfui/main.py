
from flask import Flask
from flask import request
from .backends import Backend
from .pages import Page
import yaml
import os

if os.environ.get("GF_CONFIG_FILE"):
    CONFIG_FILE = os.environ.get("GF_CONFIG_FILE")
else:
    CONFIG_FILE = "./config.yml"

app = Flask(__name__)
def Start():
    return app


def backend_from_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            c = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

    b = Backend()
    options = c['backend']['config']
    t = c['backend']['type']
    return b.get(t, OPTIONS=options)

def page_setup(template="test.html"):
    p = Page(header_template="header.html", body_template=template, footer_template="footer.html")
    p.add_nav_button("/topn_sum?f=dst_ip&sum=in_bytes", "Graph by Sum")
    p.add_nav_button("/flow", "Flows")
    return p

@app.route('/')
def index():
    return flow_search()

@app.route('/flow')
def flow_search():
    b = backend_from_config(CONFIG_FILE)
    p = page_setup("flow_table.html")

    # Form setup for this page
    f = p.register_form()
    search = f.register_input("search", "text")
    topn_max = f.register_input("max", "int")
    start_time = f.register_input("start-time", "text")
    end_time = f.register_input("end-time", "text")
    search.default = "Search"
    topn_max.default = 10
    f.parse(request.args)
    b.add_filter(op=">", value=start_time.value)
    b.add_filter(op="<", value=end_time.value)
    b.add_filter(op=None, value=search.value)

    t = b.flow_table(topn_max.value)

    form = {
        "current": f.inputs
    }

    return p.render_page(table=t, forms=form)


@app.route('/topn_sum')
def topn_sum():
    b = backend_from_config(CONFIG_FILE)
    p = page_setup("sum_graph.html")

    # Form setup for this page
    f = p.register_form()
    topn_max = f.register_input("max", "int")
    field = f.register_input("f", "text")
    sum = f.register_input("sum", "text")
    start_time = f.register_input("start-time", "text")
    end_time = f.register_input("end-time", "text")
    search = f.register_input("search", "text")
    search.default = "Search"
    topn_max.default = 10
    f.parse(request.args)
    field = field.value
    sum = sum.value
    b.add_filter(op=">", value=start_time.value)
    b.add_filter(op="<", value=end_time.value)
    b.add_filter(op=None, value=search.value)

    g = b.topn_sum_graph(field, sum, limit=topn_max.value)
    chart = g.render()
    form = {
        "select": b.get_columns(),
        "sum_select": b.get_int_columns(),
        "current": f.inputs,
    }

    return p.render_page(chart=chart, chartname=g.name, forms=form)
