import yaml
import os

# This allows us to define an env variable to set local settings to wherever adops toolkit is deployed

# Set default
if os.getenv("ADOPSSETTINGS") is None:
    os.environ["ADOPSSETTINGS"] = "settings.yaml"

settings_file = os.environ["ADOPSSETTINGS"]

with open(settings_file, "r") as f:
    settings = yaml.load(f)