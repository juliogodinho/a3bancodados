from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_funcionario import Controller_Funcionario
from controller.controller_empresa import Controller_Empresa
from controller.controller_holerite import Controller_Holerite

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_empresa = Controller_Empresa()
ctrl_funcionario = Controller_Funcionario()
ctrl_holerite = Controller_Holerite()

def reports(opcao_relatorio:int=0):

    if opcao_relatorio == 1:
        relatorio.get_relatorio_holerite()            
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_funcionario()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_empresa()

def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:                               
        novo_holerite = ctrl_holerite.inserir_holerite()
    elif opcao_inserir == 2:
        novo_funcionario = ctrl_funcionario.inserir_funcionario()
    elif opcao_inserir == 3:
        novo_empresa = ctrl_empresa.inserir_empresa()

def atualizar(opcao_atualizar:int=0):

    if opcao_atualizar == 1:
        relatorio.get_relatorio_holerite()
        holerite_atualizado = ctrl_holerite.atualizar_holerite()
    elif opcao_atualizar == 2:
        relatorio.get_relatorio_funcionario()
        funcionario_atualizado = ctrl_funcionario.atualizar_funcionario()
    elif opcao_atualizar == 3:
        relatorio.get_relatorio_empresa()
        empresa_atualizado = ctrl_empresa.atualizar_empresa()

def excluir(opcao_excluir:int=0):

    if opcao_excluir == 1:
        relatorio.get_relatorio_holerite()
        ctrl_holerite.excluir_holerite()
    elif opcao_excluir == 2:                
        relatorio.get_relatorio_funcionario()
        ctrl_funcionario.excluir_funcionario()
    elif opcao_excluir == 3:                
        relatorio.get_relatorio_empresa()
        ctrl_empresa.excluir_empresa()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)
        
        if opcao == 1: # Relatórios
            
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-3]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros

            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4:

            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            excluir(opcao_excluir=opcao_excluir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 5:

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
    run()