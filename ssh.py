"""
Python Workspace Sync
---------------------
About:
This application leverages Python to synchronises two workspaces from source to remote over port 22.

Notes:
For the moment this is a terminal application
"""
import paramiko

class SSHHandler():

    def __init__(self) -> None:
        self.client = None

    def _client(self):

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname="127.0.0.2",
            port=2522,
            username="hawk-eye-ub",
            password="blackbird99"
        )

        self.client = client

    def _exec(self, command) -> object:
        stdin, stdout, stderr = self.client.exec_command(
            command
        )
        return {
            "stdin": stdin.readlines() if stdin.readable() else None,
            "stdout": stdout.readlines() if stdout.readable() else None,
            "stderr": stderr.readlines() if stderr.readable() else None,
        }

    def _get_file(self, src, dest):
        """
            arg:
                src: The source file on the remote host
                dest: The location to save the file on the local host
        """
        if not src:
            raise Exception(
                "src (source) cannot be empty."
            )
        if not dest:
            raise Exception(
                "dest (destination) cannot be empty."
            )
        # TODO Validate if path exists
        ftp_client = self.client.open_sftp()
        ftp_client.get(src, dest)
        ftp_client.close()

    def _put_file(self, src, dest):
        """
            arg:
                src: The source file on the local host
                dest: The location to save the file on the remote host
        """
        if not src:
            raise Exception(
                "src (source) cannot be empty."
            )
        if not dest:
            raise Exception(
                "dest (destination) cannot be empty."
            )
        # TODO Validate if path exists
        ftp_client = self.client.open_sftp()
        ftp_client.put(src, dest)

if __name__ == "__main__":

    print("Starting application...")
    ss = SSHHandler()
    ss._client()
    response = ss._exec("ls -l")
    print(response)