from paramiko import SSHClient
import time
import readchar

class SSH:
    
    def __init__(self) -> None:
        self.ssh = self.connect()
        self.channel = self.open_channel()

    def connect(self):
        '''
        Important: Connect to robot20 wifi first
        Also user needs to have connected with ssh to the robot at least once manually via terminal !
        '''
        print('Establishing Robot Connection:')
        ssh = SSHClient()
        ssh.load_system_host_keys()
        try :
            ssh.connect('10.42.0.1', username='pi', password='raspberry')
            print('Connection Established')
            return ssh
        except: 
            return None
        

    def transfer_file(self, local_filepath, outbound_filepath):
        '''
        Transfers a file to the robot
        '''

        print(f'Starting File Transfer of {local_filepath}')
        sftp = self.ssh.open_sftp()
        
        sftp.put(local_filepath, outbound_filepath)

        sftp.close()
        print('File Transfer Complete')

    def download_file(self, outbound_filepath, local_filepath):
        '''
        Downloads a file from the robot
        '''
        print(f'Starting File Transfer of {outbound_filepath}')
        sftp = self.ssh.open_sftp()
        
        sftp.get(outbound_filepath, local_filepath)

        sftp.close()
        print('File Transfer Complete')

    def run_command(self, command):
        '''
        Execute a bash command on the robot and return the output 
        '''
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(command, get_pty=True)
        ssh_stdin.close()

        return ssh_stdout.read().decode('ascii')
    
    def close(self):
        print('Closing Connection')
        self.ssh.close()

    def open_channel(self, printoutput=True):
        '''
        Opens a ssh channel to allow for executing python code and reading the output
        '''
        print('Opening channel for commands')
        try:
            channel = self.ssh.get_transport().open_session()
            channel.get_pty()
            channel.invoke_shell()
            if printoutput:
                while True:
                    if channel.recv_ready():
                        output = channel.recv(1024)
                        print(output.decode('ascii'), end="")
                    else:
                        time.sleep(0.5)
                        if not(channel.recv_ready()):
                            break

        except:
            raise Exception('Channel transport failed.')

        return channel



    def run_channel_command(self, command, printoutput=False):
        '''
        Runs commands on the ssh channel. Can be either bash or python code.
        '''
        self.channel.send(command + "\n")

        if not printoutput:
            return 
        
        output = b""
        while True:
            if self.channel.recv_ready():
                output = self.channel.recv(1024)
                print(output.decode('ascii'), end="")
            else:
                time.sleep(0.5)
                if not(self.channel.recv_ready()):
                    break


if __name__ == '__main__':
    ssh = SSH()

    # ssh.transfer_file('temp/tts.txt', 'Downloads/tts.txt')
    # ssh.transfer_file('picarx/tts.py', 'Downloads/tts.py')

    # output = ssh.run_command(command)
    # print(output)

    ssh.run_channel_command('python3', True)
    ssh.run_channel_command('2+2', True)

    ssh.close()

