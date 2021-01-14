import subprocess 


subprocess.run("python api.py & python integration_tests.py", shell=True)
