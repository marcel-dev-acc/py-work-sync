# Maintained
import env
from ssh import SSHHandler


def ssh_app(project_root):
    # SSH handler
    ss = SSHHandler()
    ss._client()
    # Sync loop
    while os.environ["RUN_SSH_APP"] == "TRUE":
        # Set application run variables
        print("Reading 'settings.json'...")
        with open(os.path.join(project_root, "settings.json"), "r") as file:
            file_contents = json.loads(file.read())
        os.environ["RUN_SSH_APP"] = "TRUE" if file_contents["RUN_SSH_APP"] else "FALSE"
        command = "du"
        if file_contents["REMOTE_COMMAND"]:
            command = file_contents["REMOTE_COMMAND"]

        # Get remote file sizes
        response = ss._exec(
            "{} {}".format(
                command,
                os.environ.get("REMOTE_HOST_FOLDER")
            )
        )
        # print(json.dumps(response, indent=4))

        stdout = response.get("stdout")
        if not stdout:
            continue
        
        # Get remote folder size on linux
        print("Calculating REMOTE_HOST_FOLDER size...")
        remote_base_folder_size = 0
        for line in stdout:
            size, folder_path = line.replace("\n", "").split("\t")
            if folder_path == os.environ.get("REMOTE_HOST_FOLDER"):
                remote_base_folder_size = size
        
        if remote_base_folder_size == 0:
            continue

        # Get local folder size, any
        print("Calculating LOCAL_HOST_FOLDER size...")
        local_base_folder_size = 0
        for path, dirs, files in os.walk(os.environ.get("LOCAL_HOST_FOLDER")):
            file_contents["LOCAL_FOLDER"][path] = 0
            for file in files:
                fp = os.path.join(path, file)
                local_base_folder_size += os.path.getsize(fp)

        if local_base_folder_size == 0:
            continue
        
        print(remote_base_folder_size)
        print(local_base_folder_size)
        if remote_base_folder_size != local_base_folder_size:
            print("Local folder out of sync with remote folder")
            # Remote remote folder
            # response = ss._exec(
            #     "rm -rf {}".format(
            #         os.environ.get("REMOTE_HOST_FOLDER")
            #     )
            # )
            # # Send folder over
            # ss._put_file(
            #     src=os.environ.get("LOCAL_HOST_FOLDER"),
            #     dest=os.environ.get("REMOTE_HOST_FOLDER")
            # )

        with open(os.path.join(project_root, "settings.json"), "r") as file:
            file.write(
                json.dumps(
                    file_contents
                )
            )

        # Sync sleep
        time.sleep(10)

    # Bring down application
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
    print("Terminating ssh_app()...")


def main_ssh():
    print("Starting application...")
    ssh_process = None
    run_ssh_process = True
    project_root = os.getcwd()

    # Initialise the settings.json file with run = True
    with open(os.path.join(project_root, "settings.json"), "r") as file:
        file_contents = json.loads(file.read())
    if not file_contents["RUN_SSH_APP"]:
        print("Application instance already exists...")
        return None
    os.environ["RUN_SSH_APP"] = "TRUE" if file_contents["RUN_SSH_APP"] else "FALSE"
    
    # Default variables
    file_contents["LOCAL_FOLDER"] = {}
    with open(os.path.join(project_root, "settings.json"), "w") as file:
        file.write(
            json.dumps(file_contents, indent=4, sort_keys=True)
        )

    folder_contents = os.listdir(project_root)
    for file in folder_contents:
        if str(file).find("ssh_process_") > -1:
            run_ssh_process = False

    if not run_ssh_process:
        print("Application instance already exists...")
        return None

    print("Starting ssh_app()...")
    ssh_process = mp.Process(
        target=ssh_app,
        args=(project_root,)
    )
    ssh_process.start()
    ssh_process.join()
    # with open(os.path.join(project_root, "ssh_process_{}.pid".format(ssh_process.pid)), "w") as file:
    #     file.write(str(ssh_process.pid))
    

if __name__ == "__main__":

    main_ssh()

    # app.run(debug=True if os.environ.get("DEBUG") == "TRUE" else False)
