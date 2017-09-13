import subprocess

process = subprocess.Popen(['./1-mycanary', ''], stdout=subprocess.PIPE)
stdout = process.communicate() 
