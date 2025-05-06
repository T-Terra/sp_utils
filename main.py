from src.args import args
from src.pre_instalacao import *

def main():
    if args.nome:
        rename(args.nome)
    
    if args.users:
        users_deactvate()

    if args.firewall:
        firewall_deactivate()
    
    if args.energia:
        power_options()
    
    if args.convidado:
        logon_deactivate()
    
    if args.reiniciar:
        restart_pc()
    
    if args.ip:
        get_interface()
        interface = str(input("Digite o nome da interface: ")).strip()
        ip_config(interface)
        dns_config(interface)
        print("Configurações de rede aplicadas com sucesso!")
    
    if args.all:
        all_config()
    
    
if __name__ == '__main__':
    main()