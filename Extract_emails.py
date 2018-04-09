import subprocess

#----------- Created By Fl337 -- BentRobotLabs
#----------- 4/9/2018

cmd = "grep -o 'mailto.*' MapLinks.txt" # ------ Change this 'MapLinks.txt' file to the one your specific links file!!!
output = subprocess.check_output(['bash', '-c', cmd])
output = output.replace('\n', ' ')

lines = output.split()

for i in range(0, len(lines)):
	#Process the lines as you wish
	lines[i] = lines[i][7:].rstrip('/')
	

new_emails = []

for i in range(0, len(lines)):
	if not lines[i] in new_emails:
		new_emails.append(lines[i])

file = open('emails.txt', 'w')
file.write("\n".join(new_emails))
file.close()

