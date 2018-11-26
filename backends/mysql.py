from .default import Backend
import mysql.connector
from chartgraph import Graph

class Mysql_backend(Backend):
    def __init__(self, OPTIONS):
        super().__init__()
        print("Got this far")
        self.required_opts = ['host', 'user', 'passwd', 'db']
        self.parse_options(OPTIONS)
        self.columns = {}

        self.db = mysql.connector.connect(
            host=self.OPTIONS['host'],
            user=self.OPTIONS['user'],
            passwd=self.OPTIONS['passwd']
        )
        self.schema = Schema()

    def topn_graph(self, field):
        db = self.db
        FLOWS_PER_IP = self.schema.topn(field)

        cursor = db.cursor()
        cursor.execute("USE testgoflow")
        cursor.execute(FLOWS_PER_IP)
        r = cursor.fetchall()
        g = Graph()
        g.name = "topn_{0}".format(field)
        g.graph_from_rows(r, 0)
        return g

    def topn_sum_graph(self, field, sum_by):
        db = self.db
        FLOWS_PER_IP = self.schema.topn_sum(field, sum_by)

        cursor = db.cursor()
        cursor.execute("USE testgoflow")
        cursor.execute(FLOWS_PER_IP)
        r = cursor.fetchall()
        g = Graph()
        g.name = "topn_{0}".format(field)
        g.graph_from_rows(r, 0)
        return g


class Column:
    """
    Column

    Column handling class.
    Governs how query strings are built and helper functons for returned data.
    """
    def __init__(self, name):
        self.name = name

    def select(self):
        return "{0}".format(self.name)


class IP4Column(Column):
    def __init__(self, name):
        super().__init__(name)

    def select(self):
        return "inet_ntoa({0})".format(self.name)


class Schema:
    """
    Schema

    Defines the backend schema
    Changes to the backend (naming, etc.) should be reflected here.
    """
    def __init__(self):
        # Default
        self.limit = 10

        # Columns
        self.columns = {
            "last_switched": Column("last_switched"),
            "src_ip": IP4Column("src_ip"),
            "src_port": Column("src_port"),
            "dst_ip": IP4Column("dst_ip"),
            "dst_port": Column("dst_port"),
            "in_bytes": Column("in_bytes"),
        }

        # Supported queries
        self.QUERIES = {
            "TOPN": self.topn
        }

    def topn(self, column):
        count = "last_switched"
        q = """
        SELECT {0}, count({1}) AS c FROM goflow_records GROUP BY {0} ORDER BY c DESC
        """.format(self.columns[column].select(), count)
        return self.query_boilerplate(q)

    def topn_sum(self, column, sum_by):
        q = """
        SELECT {0}, sum({1}) AS c FROM goflow_records GROUP BY {0} ORDER BY c DESC
        """.format(self.columns[column].select(), sum_by)
        return self.query_boilerplate(q)

    def query_boilerplate(self, q):
        q = q + """LIMIT {0}""".format(self.limit)
        return q
