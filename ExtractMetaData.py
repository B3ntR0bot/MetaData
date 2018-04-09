import subprocess

#----------- Created By Fl337 -- BentRobotLabs
#----------- 4/9/2018

file = open('/root/Desktop/Datto/pdf_links.txt')
lines = []
for line in file:
	line = line.strip()
	lines.append(line)

for i in range(0, len(lines)):
	cmd = "wget " + lines[i] + " -P /root/Desktop/Datto/PDF"
	output = subprocess.check_output(['bash', '-c', cmd])

cmd = "cd /root/Desktop/Datto/PDF/ && ls"
dirs = subprocess.check_output(['bash', '-c', cmd])

#All these lines do is replace spaces with '_' so during the split process
#a pdf name like 'hi im a pdf' wont be turned into 'hi' 'im' 'a' 'pdf'.
#--------------------------------------------------------------------------

dirs = dirs.replace('_', '?')
dirs = dirs.replace(' ', '_')
dirs = dirs.replace('\n', ' ')
list = dirs.split()

cmd = "cd /root/Desktop/Datto/PDF/ && exiftool "

for i in range(0, len(list)):
	
	#Put spaces back to open correct pdf
	#-----------------------------------
	temp = list[i].replace('_', ' ')
	temp = temp.replace('?', '_')
	cmd = cmd + "'" + temp + "' "	


cmd = cmd + " >> /root/Desktop/Datto/pdf_metadata.txt"
subprocess.check_output(['bash', '-c', cmd])

file.close()

