from lib.SSH import SSH


if __name__ == "__main__":
    ssh = SSH()
    ssh.download_file(outbound_filepath="picar-x/example/4.avoiding_obstacles.py", local_filepath='4.avoiding_obstacles.py')
    print('Download Complete')
    
