from paramiko import SSHClient
import time

'''
Resources: 
https://stackoverflow.com/questions/63134910/responding-to-an-input-when-executing-a-python-script-through-ssh
'''

class SSH:
    
    def __init__(self) -> None:
        self.ssh = self.connect()

    def connect(self):
        print('Establishing Robot Connection:')
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect('10.42.0.1', username='pi', password='raspberry')
        print('Connection Established')
        return ssh

    def transfer_file(self, local_filepath, outbound_filepath):
        print(f'Starting File Transfer of {local_filepath}')
        sftp = self.ssh.open_sftp()
        
        sftp.put(local_filepath, outbound_filepath)

        sftp.close()
        print('File Transfer Complete')

    def upload_file(self, local_filepath, outbound_filepath):
        print(f'Starting File Transfer of {local_filepath}')
        sftp = self.ssh.open_sftp()
        
        sftp.put(local_filepath, outbound_filepath)

        sftp.close()
        print('File Transfer Complete')

    def download_file(self, outbound_filepath, local_filepath):
        print(f'Starting File Transfer of {outbound_filepath}')
        sftp = self.ssh.open_sftp()
        
        sftp.get(outbound_filepath, local_filepath)

        sftp.close()
        print('File Transfer Complete')

    def run_command(self, command):
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(command, get_pty=True)
        ssh_stdin.close()
        # print(ssh_stdout.read().decode('ascii')) #print the output of command

        return ssh_stdout.read().decode('ascii')
    
    def close(self):
        print('Closing Connection')
        self.ssh.close()

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
    
