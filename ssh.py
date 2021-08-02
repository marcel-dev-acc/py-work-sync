"""
Python Workspace Sync
---------------------
About:
This application leverages Python to synchronises two workspaces from source to remote over port 22.

Notes:
For the moment this is a terminal application
"""
import os
import paramiko

class SSHHandler:

    def __init__(self) -> None:
        
        
        # Validate incoming environment variables
        hostname = os.environ.get("HOSTNAME")
        if not hostname:
            raise ValueError("Define HOSTNAME in env variable list")
        port = os.environ.get("PORT")
        if not port:
            raise ValueError("Define PORT in env variable list")
        username = os.environ.get("USERNAME")
        if not username:
            raise ValueError("Define USERNAME in env variable list")
        password = os.environ.get("PASSWORD")
        if not password:
            raise ValueError("Define PASSWORD in env variable list")

        # Defined initialisation parameters
        self.client = None
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def _client(self):
        """_client wraps the .connect()"""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password
        )
        self.client = client

    def _exec(self, command) -> object:
        """"""
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
            _get_file wraps the open_sftp() and .get() methods for file
            transmission between a remote host and a local host.

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
            _put_file wraps the open_sftp() and .get() methods for file
            transmission between a local host and a remote host.

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
    print("Ending application...")