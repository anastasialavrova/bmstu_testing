import subprocess 


subprocess.run("python integration/api.py & python integration/e2e_tests.py", shell=True)
