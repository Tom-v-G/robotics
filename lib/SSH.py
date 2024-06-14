from paramiko import SSHClient
import time
import readchar

'''
Resources: 
https://stackoverflow.com/questions/63134910/responding-to-an-input-when-executing-a-python-script-through-ssh
'''

class SSH:
    
    def __init__(self) -> None:
        self.ssh = self.connect()
        self.channel = self.open_channel()

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

    def open_channel(self, printoutput=True):
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
        #return output.decode('ascii')

        # print("give command")
        # while True:
        #     key = input()
        #     if key == 'q':
        #         break
        #     else: 
        #         command = key
        #         print(f"executing {command}")
        #         stdin, stdout, stderr = self.ssh.exec_command(command, get_pty=False)
        #         # print(stdout)
        #         for l in stdout :
        #              print("stdout : %s" % l.strip())
        #         # for l in stderr:
        #         #     print("stderr : %s" % l.strip())


        # while True:
        #     command = input('')
        #     if command == 'exit':
        #         break

        #     channel.send(command + "\n")

        #     while True:
        #         if channel.recv_ready():
        #             output = channel.recv(1024)
        #             print(output.decode('ascii'), end="")
        #         else:
        #             time.sleep(0.5)
        #             if not(channel.recv_ready()):
        #                 break

        # self.ssh.close()
    
    def mobile_robot_challenge(self):
        channel = self.ssh.get_transport().open_session()
        channel.get_pty()
        channel.invoke_shell()

        command = '''
        python3 picar-x/example/Robot_FP.py
        '''
        channel.send(command + "\n")

        if channel.recv_ready():
            output = channel.recv(1024)
            print(output.decode('ascii'), end="")
        channel.send('\n')

        if channel.recv_ready():
            output = channel.recv(1024)
            print(output.decode('ascii'), end="")

        while True:
            key = readchar.readkey().lower()
            
            channel.send(key)
            if channel.recv_ready():
                    output = channel.recv(1024)
                    print(output.decode('ascii'), end="")
            if key == 'q':
                time.sleep(0.5)
                break
        
        self.download_file('Videos/picarx_recording.avi', 'temp/video.avi')
            # else:
            #     time.sleep(0.5)
            #     if not(channel.recv_ready()):
            #         break


if __name__ == '__main__':
    ssh = SSH()

    # ssh.transfer_file('temp/tts.txt', 'Downloads/tts.txt')
    # ssh.transfer_file('picarx/tts.py', 'Downloads/tts.py')

    
    #ssh.mobile_robot_challenge()
    # output = ssh.run_command(command)
    # print(output)

    ssh.run_channel_command('python3')





    ssh.close()

