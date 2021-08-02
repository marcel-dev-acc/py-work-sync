import env
from ssh import SSHHandler
from flask import Flask
from flask import render_template
import os
import json
import time
import multiprocessing as mp

app = Flask(__name__)

###########################################################
# ROUTES
###########################################################

@app.route("/", methods=["GET"])
def index():
    contents = {
        "page_title": "Application Settings Page",
    }
    return render_template('index.html', contents=contents)





###########################################################
# SSH APP & __main__
###########################################################

def ssh_app(project_root):
    # SSH handler
    ss = SSHHandler()
    ss._client()
    # Sync loop
    while os.environ["RUN_SSH_APP"] == "TRUE":
        print("Reading 'settings.json'...")
        with open(os.path.join(project_root, "settings.json"), "r") as file:
            file_contents = json.loads(file.read())
        os.environ["RUN_SSH_APP"] = "TRUE" if file_contents["RUN_SSH_APP"] else "FALSE"
        print(
            "Environment VAR RUN_SSH_APP is: {}".format(
                os.environ["RUN_SSH_APP"]
            )
        )
        response = ss._exec(
            "du {}".format(
                os.environ.get("REMOTE_HOST_FOLDER")
            )
        )
        print(json.dumps(response, indent=4))
        time.sleep(10)

    print("Gracefully bringing down ssh_app()")
    folder_contents = os.listdir(project_root)
    files_to_remove = []
    for file in folder_contents:
        if str(file).find("ssh_process_") > -1:
            files_to_remove.append(file)
            break

    for file in files_to_remove:
        os.remove(
            os.path.join(
                project_root,
                file
            )
        )
    print("Terminating ssh_app...")


if __name__ == "__main__":

    print("Starting application...")
    ssh_process = None
    run_ssh_process = True
    project_root = os.getcwd()

    # Initialise the settings.json file with run = True
    with open(os.path.join(project_root, "settings.json"), "w") as file:
        file.write(
            json.dumps({})
        )
    with open(os.path.join(project_root, "settings.json"), "r") as file:
        file_contents = json.loads(file.read())
        print(file_contents)
    file_contents["RUN_SSH_APP"] = True
    os.environ["RUN_SSH_APP"] = "TRUE"
    with open(os.path.join(project_root, "settings.json"), "w") as file:
        file.write(
            json.dumps(file_contents, indent=4, sort_keys=True)
        )

    folder_contents = os.listdir(project_root)
    files_to_remove = []
    for file in folder_contents:
        if str(file).find("ssh_process_") > -1:
            run_ssh_process = False

    if run_ssh_process:
        print("Starting ssh_app...")
        ssh_process = mp.Process(
            target=ssh_app,
            args=(project_root,)
        )
        ssh_process.start()
        with open(os.path.join(project_root, "ssh_process_{}.pid".format(ssh_process.pid)), "w") as file:
            file.write(str(ssh_process.pid))

    app.run(debug=True if os.environ.get("DEBUG") == "TRUE" else False)
        
