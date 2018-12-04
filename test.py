
import os
from flask import Flask
from flask import request
from backends import Backend
from pages import Page

app = Flask(__name__)


backends = Backend()
pw = os.environ.get("SQL_PASSWORD")
options = {
    "host": "52.62.226.159",
    "user": "testgoflow",
    "passwd": pw,
    "db": "testgoflow"
}
b = backends.get("mysql", OPTIONS=options)


def page_setup(template="test.html"):
    p = Page(header_template="header.html", body_template=template, footer_template="footer.html")
    p.add_nav_button("/topn?f=dst_ip", "Graph by Flows")
    p.add_nav_button("/topn_sum?f=dst_ip&sum=in_bytes", "Graph by Sum")
    return p


@app.route('/topn')
def topn():
    """
    Topn graph is the top N results for query based on amount of flows
    :return: HTML
    """
    p = page_setup("graph.html")

    f = p.register_form()
    topn_max = f.register_input("max", "int")
    field = f.register_input("f", "text")
    topn_max.default = 10
    f.parse(request.args)

    g = b.topn_graph(field.value, topn_max.value)

    chart = g.render()
    form = {
        "select": b.get_columns(),
        "current": f.inputs,
    }

    return p.render_page(chart=chart, chartname=g.name, forms=form)


@app.route('/topn_sum')
def topn_sum():
    p = page_setup("sum_graph.html")

    f = p.register_form()
    topn_max = f.register_input("max", "int")
    field = f.register_input("f", "text")
    sum = f.register_input("sum", "text")
    topn_max.default = 10
    f.parse(request.args)
    field = field.value
    sum = sum.value

    g = b.topn_sum_graph(field, sum)
    chart = g.render()
    form = {
        "select": b.get_columns(),
        "sum_select": b.get_int_columns(),
        "current": f.inputs,
    }

    return p.render_page(chart=chart, chartname=g.name, forms=form)
