"""The method opens the .env file located in
the root of the project and loads them as
environment variables for use throughout the
project.
The idea is that this file is run on import alone."""

import os

dot_env_file_path = os.path.join(
    os.getcwd(),
    ".env"
)
with open(dot_env_file_path, "r") as dot_env:
    dot_env_contents = dot_env.read()
# Set environment variables
for line in dot_env_contents.split("\n"):
    key, value = line.split("=")
    os.environ[key] = value