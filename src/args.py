import argparse

parser = argparse.ArgumentParser(description="Utilitario pre-instalacao")

parser.add_argument('-n', '--nome', type=str, help='Renomear computador')
parser.add_argument('-r', '--reiniciar', action='store_true', help='Reiniciar o computador depois da configuracao.')
parser.add_argument('-u', '--users', action='store_true', help='Desativar usuarios e verificar se ADM esta ativo.')
parser.add_argument('-f', '--firewall', action='store_true', help='Configuracoes de firewall')
parser.add_argument('-e', '--energia', action='store_true', help="Configurar opções de energia")
parser.add_argument('-c', '--convidado', action='store_true', help='Permitir conexões de convidados e senhas em branco')
parser.add_argument('-i', '--ip', action='store_true', help='Configura IP e DNS')
parser.add_argument('-a', '--all', action='store_true', help='Executa todas as configurações')


args = parser.parse_args()