"""
This main function servers as an entry point and step-wise
manipulation of all sub-processes.
"""
# Modules
import env
from ssh import SSHHandler
from local_folders import list_folder as list_local_folder
from remote_folders import list_folder as list_remote_folder
from comparison import comparison
from sync import forward_sync

# Installed Packages
import os
import json
from datetime import datetime
import time

if __name__ == "__main__":
    while True:
        # Log start time
        start_date_time = datetime.now()
        print("Start date time:", start_date_time)
        # Load local folders for comparison
        folder_contents_list = list_local_folder(
            os.environ.get("LOCAL_HOST_FOLDER")
        )
        with open(os.path.join(os.getcwd(), "local_tree.json"), "w") as file:
            file.write(json.dumps(folder_contents_list, indent=4))
        print("Finished loading local folders")

        # Load remote folders for comparison
        ss = SSHHandler()
        ss._client()
        folder_contents_list = list_remote_folder(
            ss,
            os.environ.get("REMOTE_HOST_FOLDER")
        )
        with open(os.path.join(os.getcwd(), "remote_tree.json"), "w") as file:
            file.write(json.dumps(folder_contents_list, indent=4))
        print("Finished loading remote folders")

        # Compare the two folder structures
        matched = comparison()
        print("Matched status:", matched)
        if not matched:
            # Remove folder completely if it exists
            ss._exec(
                "rm -rf {}".format(os.environ.get("REMOTE_HOST_FOLDER"))
            )
            ss._exec(
                "mkdir -p {}".format(os.environ.get("REMOTE_HOST_FOLDER"))
            )
            # Reload remote folder
            folder_contents_list = list_remote_folder(
                ss,
                os.environ.get("REMOTE_HOST_FOLDER")
            )
            with open(os.path.join(os.getcwd(), "remote_tree.json"), "w") as file:
                file.write(json.dumps(folder_contents_list, indent=4))
            print("Finished loading remote folders")
            # Sync folders
            forward_sync(ss)

        end_date_time = datetime.now()
        print("End date time:", end_date_time)
        print("Code execution duration:", (end_date_time - start_date_time))
        print("------------------")
        time.sleep(5)