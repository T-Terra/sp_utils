import os
from src.utils.terminal import run_cmd, run
from time import sleep


def rename(newname: str):
    oldname = os.environ['COMPUTERNAME']
    print(f"Nome atual do computador: {oldname}")
    print(f"Renomeando computador para {newname}...")
    run(f'rename-computer -newname "{newname}" -force')
    print(f"Finalizado!")

def users_deactvate():
    # 2. Ativar 'Administrador' e desativar outros usuários locais
    users = run('Get-WmiObject -Class Win32_UserAccount -Filter "LocalAccount=True" | Select-Object -ExpandProperty Name').stdout.splitlines()

    for user in users:
        user = user.strip()
        if user.lower() == "administrador":
            status = run("(Get-LocalUser -Name 'Administrador').Enabled").stdout.strip()
            if status.lower() == "false":
                print("Ativando Administrador...")
                run("Enable-LocalUser -Name 'Administrador'")
            else:
                print("Administrador ativo OK.")
        else:
            print(f"Desabilitando {user}...")
            run(f'Disable-LocalUser -Name "{user}"')

def firewall_deactivate():
    # 3. Desativar firewall para todos os perfis
    print("Iniciando Configurações de Firewall...")
    run_cmd("netsh advfirewall set domainprofile state off")
    run_cmd("netsh advfirewall set privateprofile state off")
    run_cmd("netsh advfirewall set publicprofile state off")
    print("Configurações aplicadas com sucesso!")

def power_options():
    # 4. Configurar opções de energia
    # Nunca desligar vídeo
    run_cmd("powercfg /change monitor-timeout-ac 0")
    run_cmd("powercfg /change monitor-timeout-dc 0")

    # Nunca suspender o computador
    run_cmd("powercfg /change standby-timeout-ac 0")
    run_cmd("powercfg /change standby-timeout-dc 0")

    # Nunca hibernar
    run_cmd("powercfg /change hibernate-timeout-ac 0")
    run_cmd("powercfg /change hibernate-timeout-dc 0")

    # Nunca desligar disco rígido
    run_cmd("powercfg /change disk-timeout-ac 0")
    run_cmd("powercfg /change disk-timeout-dc 0")

    # Desativar suspensão híbrida
    run_cmd("powercfg /setacvalueindex SCHEME_BALANCED SUB_SLEEP HYBRIDSLEEP 0")
    run_cmd("powercfg /setdcvalueindex SCHEME_BALANCED SUB_SLEEP HYBRIDSLEEP 0")

    print("Opções de energia configuradas com sucesso!")

def logon_deactivate():
    # 5. Alterar registros para permitir login com senha em branco
    run_cmd(r'reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v LimitBlankPasswordUse /t REG_DWORD /d 0 /f')

    # 6. Permitir conexões de convidados
    run_cmd(r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters" /v AllowInsecureGuestAuth /t REG_DWORD /d 1 /f')

    print("Compartilhamento protegido por senha desativado com sucesso!")

def restart_pc():
    print("Reiniciando a máquina...")
    sleep(5)
    run_cmd("shutdown /r /t 0")

def all_config():
    newNamePc = str(input("Digite o nome do PC: ")).strip().upper()
    rename(newNamePc)
    users_deactvate()
    firewall_deactivate()
    power_options()
    logon_deactivate()
    get_interface()
    interface = str(input("Digite o nome da interface: ")).strip()
    ip_config(interface)
    dns_config(interface)
    restart_pc()

def ip_config(interface: str):
    ip = str(input("Digite o ip ex[192.168.1.100]: ")).strip()
    mask = "255.255.255.0"
    gateway = str(input("Digite o gateway padrão ex[192.168.1.1]: ")).strip()
    command_ip = f"netsh interface ip set address name={interface} static {ip} {mask} {gateway}"
    run_cmd(command_ip)

def dns_config(interface: str):
    dns_first = str(input("Digite o DNS 1 ex[8.8.8.8]: ")).strip()
    dns_second = str(input("Digite o DNS 2 ex[8.8.4.4]: ")).strip()

    command_dns_first = f"netsh interface ip set dnsservers name={interface} static address={dns_first} primary"

    run_cmd(command_dns_first)

    command_dns_second = f"netsh interface ip add dnsservers name={interface} address={dns_second}"

    run_cmd(command_dns_second)

def get_interface():
    result = run_cmd("netsh interface show interface")
    interface_names = []

    if result.returncode == 0:
        lines = result.stdout.strip().splitlines()
        name_i = lines[2:][0].split(" ")[-1]
        interface_names.append(name_i)

        print("Interfaces encontradas:")
        for name in interface_names:
            print(name)
    else:
        print("Erro ao executar o comando:")
        print(result.stderr)