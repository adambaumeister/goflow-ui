from backends import Schema
import re

s = "dst 152.83.247.1 src 138.194.0.0/16"
if re.search("dst (\d+\.\d+\.\d+\.\d+\/\d+|\d+\.\d+\.\d+\.\d+)", s):
    print("yes")


s = Schema()
s.add_filter("dst 152.83.247.1 src 138.194.0.0/16")
print(s.build_filter_string())
