from paramiko import SSHClient


ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('user@server:path')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls -l')
print(ssh_stdout) #print the output of ls command

# https://stackoverflow.com/questions/68335/how-to-copy-a-file-to-a-remote-server-in-python-using-scp-or-ssh
# https://www.tutorialspoint.com/What-is-the-simplest-way-to-SSH-using-Python
# https://docs.python.org/3/library/subprocess.html

''' SCP using Paramiko: 
ssh.connect(server, username=username, password=password)
sftp = ssh.open_sftp()
sftp.put(localpath, remotepath)
sftp.close()
ssh.close(
'''

''' SCP using subprocess
import subprocess
subprocess.run(["scp", FILE, "USER@SERVER:PATH"])
#e.g. subprocess.run(["scp", "foo.bar", "joe@srvr.net:/path/to/foo.bar"])

'''