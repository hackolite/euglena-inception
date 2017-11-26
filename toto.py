import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
        ssh.connect('localhost', username='llaureote', password='Babarlesource972')
except paramiko.SSHException:
        print("Connection Failed")
        quit()

stdin,stdout,stderr = ssh.exec_command("ls /etc/")

for line in stdout.readlines():
        print(line.strip())
ssh.close()
