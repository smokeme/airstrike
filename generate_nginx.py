## This script generates the nginx configuration file for the backend specified in the config.py file
# read the config file

import backend.config as config
C2 = config.C2
path = C2.get("path")
# Ensure path is properly fetched and is a string
if path is None:
    raise ValueError("Path not found in C2 configuration")

# This is the nginx configuration file
nginx_config = """
    location /{path}/ {{
        proxy_pass http://127.0.0.1:23000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }}
""".format(path=path)

print(nginx_config)
