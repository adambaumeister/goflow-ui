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

    def get_columns(self):
        return self.schema.get_columns()

    def get_int_columns(self):
        return self.schema.get_int_columns()

    def topn_graph(self, field, limit=10):
        db = self.db
        self.schema.limit = limit
        FLOWS_PER_IP = self.schema.topn(field)

        cursor = db.cursor()
        cursor.execute("USE testgoflow")
        cursor.execute(FLOWS_PER_IP)
        r = cursor.fetchall()
        g = Graph()
        g.name = "topn_{0}".format(field)
        g.graph_from_rows(r, 0)
        return g

    def topn_sum_graph(self, field, sum_by, limit=10):
        db = self.db
        self.schema.limit = limit
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
    def __init__(self, name, display_name=None):
        self.name = name
        self.display_name = display_name
        self.type = 'text'

    def get_display_name(self):
        return self.display_name

    def select(self):
        return "{0}".format(self.name)


class IP4Column(Column):
    def __init__(self, name, display_name=None):
        super().__init__(name, display_name)
        self.type = "ip"

    def select(self):
        return "inet_ntoa({0})".format(self.name)

class IntColumn(Column):
    def __init__(self, name, display_name=None):
        super().__init__(name, display_name)
        self.type = 'int'

    def select(self):
        return "{0}".format(self.name)

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
            "last_switched": Column("last_switched", "Last Switched"),
            "src_ip": IP4Column("src_ip", "Source IP"),
            "src_port": Column("src_port", "Source Port"),
            "dst_ip": IP4Column("dst_ip", "Destination IP"),
            "dst_port": Column("dst_port", "Destination Port"),
            "in_bytes": IntColumn("in_bytes", "Input bytes"),
        }

        # Supported queries
        self.QUERIES = {
            "TOPN": self.topn
        }

    def get_columns(self):
        result = {}
        for col_name, col in self.columns.items():
            result[col_name] = col.get_display_name()

        return result

    def get_int_columns(self):
        result = {}
        for col_name, col in self.columns.items():
            if col.type is "int":
                result[col_name] = col.get_display_name()

        return result

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
