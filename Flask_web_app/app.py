import subprocess

subprocess.Popen("python main.py", shell=True)
subprocess.Popen("python publisher.py", shell=True)
subprocess.Popen("python subscriber.py", shell=True)