
import os
from flask import Flask
from flask import render_template
from chartgraph import Graph
from backends import Backend


backends = Backend()
pw = os.environ.get("SQL_PASSWORD")
options = {
    "host": "52.62.226.159",
    "user": "testgoflow",
    "passwd": pw,
    "db": "testgoflow"
}
b = backends.get("mysql", OPTIONS=options)
r = b.topn_graph()
print(r)
app = Flask(__name__)

@app.route('/')
def test():
    r = b.topn_graph()
    g = Graph()
    g.graph_from_rows(r, 0)
    c = { "labels": g.labels, "data": g.data }
    return render_template("test.html", items=c)