import subprocess

def run(cmd):
    """Executa comando no PowerShell"""
    return subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)

def run_cmd(cmd):
    """Executa comando no CMD"""
    return subprocess.run(cmd, shell=True)