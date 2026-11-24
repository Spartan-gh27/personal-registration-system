from time import sleep
from exercicios.ex019.crud import *

def exibir_menu():
    print("\n"+"="*30)
    print("     SISTEMA DE CADASTRO")
    print("="*30)
    print("1 - Cadastrar pessoa")
    print("2 - Listar pessoas")
    print("3 - Atualizar pessoa")
    print("4 - Excluir pessoa")
    print("5 - Buscar por nome")
    print("0 - Sair")
    print("="*30)

def main():

    #cadastro_em_massa() # [IMPORTANTE] Execute apenas uma vez;

    if not criar_banco():
        print("Algum problema aconteceu ao criar o banco")
        raise SystemExit

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1": # Cadastrar pessoa
                if not cadastrar_pessoa():
                    print("\n\033[31m[ERRO] Não foi possível cadastrar a pessoa\033[m")

            case "2": # Listar pessoa
                if not listar_pessoas():
                    print("\n\033[31m[ERRO] Não foi possível mostrar a listagem\033[m")

            case "3": # Atualizar pessoa
                if not atualizar_pessoa():
                    print("\n\033[31m[ERRO] Não foi possível atualizar o cadastro\033[m")

            case "4": # Excluir pessoa
                if not excluir_pessoa():
                    print("\n\033[31m[ERRO] Não foi possível excluir a pessoa\033[m")

            case "5": # Busca por nome
                if not buscar_pessoa_por_nome():
                    print("\n\033[31m[ERRO] Não foi possível buscar os dados\033[m")

            case "0": # Sair
                print("\nEncerrando o sistema...")
                break

            case _:
                print("\n\033[31m[ERRO] Opção inválida! Escolha um valor entre 0 a 5!\033[m")

        sleep(1)
if __name__ == "__main__":
    main()