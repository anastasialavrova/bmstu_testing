import subprocess 


subprocess.run("python integration/api.py & python integration/integration_tests.py", shell=True)
