
import os
from flask import Flask
from flask import render_template
from flask import request
from backends import Backend
from pages import Page

backends = Backend()
pw = os.environ.get("SQL_PASSWORD")
options = {
    "host": "52.62.226.159",
    "user": "testgoflow",
    "passwd": pw,
    "db": "testgoflow"
}
b = backends.get("mysql", OPTIONS=options)
app = Flask(__name__)
p = Page(header_template="header.html", body_template="test.html", footer_template="footer.html")
p.add_nav_button("/topn?f=dst_ip", "Graphs")
p.add_nav_button("/topn_sum?f=dst_ip&sum=bytes", "Graph Sum")


@app.route('/topn')
def topn():
    field = request.args['f']

    g = b.topn_graph(field)
    chart = g.render()
    return p.render_page(chart=chart, chartname=g.name)

@app.route('/topn_sum')
def topn_sum():

    field = request.args['f']
    sum = request.args['sum']
    g = b.topn_sum_graph(field, sum)
    chart = g.render()

    return p.render_page(chart=chart, chartname=g.name)
