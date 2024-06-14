from lib.SSH import SSH

if __name__ == '__main__':
    ssh = SSH()
    ssh.transfer_file('picarx/Robot.py', 'picar-x/Project/Robot.py')
    ssh.close()