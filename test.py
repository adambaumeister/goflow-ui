
import os
from flask import Flask
from flask import render_template
from flask import request
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
app = Flask(__name__)

@app.route('/topn')
def test():
    field = request.args['f']
    g = b.topn_graph(field)
    chart = g.render()
    print(g.name)
    return render_template("test.html", chart=chart, chartname=g.name)