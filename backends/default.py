import backends

class Backend():
    def __init__(self):
        self.required_opts = []
        self.type_map = {
            "mysql": backends.Mysql_backend
        }

    def get(self, backend_type, OPTIONS=None):
        return self.type_map[backend_type](OPTIONS)

    def parse_options(self, OPTIONS):

        if OPTIONS:
            for opt in self.required_opts:
                if opt not in OPTIONS:
                    raise ValueError("Missing option {0} to backend.".format(opt))
        else:
            raise ValueError("Missing backend options.")

        self.OPTIONS = OPTIONS
