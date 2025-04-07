import subprocess
result = subprocess.run(["ping","baidu.com"],capture_output=True,text=True)
print(result.returncode)
print(result.stdout)
print(result.stderr)