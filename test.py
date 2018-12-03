
import os
from flask import Flask
from flask import render_template
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
    p.add_nav_button("/topn?f=dst_ip", "Graphs")
    p.add_nav_button("/topn_sum?f=dst_ip&sum=in_bytes", "Graph Sum")
    return p


@app.route('/topn')
def topn():
    p = page_setup("graph.html")
    field = request.args['f']

    g = b.topn_graph(field)
    chart = g.render()
    form = {
        "select": b.get_columns(),
    }

    return p.render_page(chart=chart, chartname=g.name, forms=form)


@app.route('/topn_sum')
def topn_sum():
    p = page_setup()
    field = request.args['f']
    sum = request.args['sum']
    g = b.topn_sum_graph(field, sum)
    chart = g.render()

    return p.render_page(chart=chart, chartname=g.name)
