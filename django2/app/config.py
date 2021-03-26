import os


DEBUG = False
env = os.environ.get("ENV")
if env == "DEV":
    DEBUG=True
else:
    DEBUG = False

