import env
from ssh import SSHHandler



if __name__ == "__main__":

    print("Starting application...")
    ss = SSHHandler()
    ss._client()
    response = ss._exec("ls -l")
    print(response)
    print("Ending application...")