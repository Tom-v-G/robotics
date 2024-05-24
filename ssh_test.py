import lib.SSH as SSH

if __name__ == '__main__':
    ssh = SSH()
    
    ssh.transfer_file('tts.txt', 'Downloads/tts.txt')
    ssh.transfer_file('picarx/tts.py', 'Downloads/tts.py')

    command = f'''
    sudo python3 Downloads/tts.py
    '''
    
    output = ssh.run_command(command)
    print(output)

    ssh.close()
    


# https://stackoverflow.com/questions/68335/how-to-copy-a-file-to-a-remote-server-in-python-using-scp-or-ssh
# https://www.tutorialspoint.com/What-is-the-simplest-way-to-SSH-using-Python
# https://docs.python.org/3/library/subprocess.html

''' SCP using Paramiko: 
ssh.connect(server, username=username, password=password)
sftp = ssh.open_sftp()
sftp.put(localpath, remotepath)
sftp.close()
ssh.close()
'''

''' SCP using subprocess
import subprocess
subprocess.run(["scp", FILE, "USER@SERVER:PATH"])
#e.g. subprocess.run(["scp", "foo.bar", "joe@srvr.net:/path/to/foo.bar"])

'''