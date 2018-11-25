from .default import Backend
import mysql.connector

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

    def topn_graph(self):
        db = self.db
        FLOWS_PER_IP = self.schema.topn("dst_ip")

        cursor = db.cursor()
        cursor.execute("USE testgoflow")
        cursor.execute(FLOWS_PER_IP)
        r = cursor.fetchall()
        return r


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
        self.limit = 50

        # Columns
        self.columns = {
            "last_switched": Column("last_switched"),
            "src_ip": IP4Column("src_ip"),
            "src_port": Column("src_port"),
            "dst_ip": IP4Column("dst_ip"),
            "dst_port": Column("dst_port")
        }
        # Supported queries
        self.QUERIES = {
            "TOPN": self.topn
        }

    def topn(self, column):
        q = """
        SELECT {0}, count(last_switched) last_switched FROM goflow_records group by {0}
        """.format(self.columns[column].select())
        return self.query_boilerplate(q)

    def query_boilerplate(self, q):
        q = q + """LIMIT {0}""".format(self.limit)
        return q
