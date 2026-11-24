import sqlite3
#from asyncio import exceptions
#from time import sleep

NOME_BANCO = "cadastro.db"

def criar_banco() -> bool:
    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cursor = db.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS pessoas (cod INTEGER PRIMARY KEY 
            AUTOINCREMENT, nome TEXT NOT NULL, altura REAL NOT NULL);""")
            return True
    except sqlite3.Error as erro:
        print(f"Falha na criação do banco: {erro}")
        return False

def cadastro_em_massa():
    cad_pessoas = [
        ("1", "Gustavo", "1.84"),
        ("2", "Gabriela", "1.63"),
        ("3", "Pedro", "2.02"),
        ("4", "Mariana", "1.72")
    ]

    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cursor = db.cursor()
            cursor.executemany("INSERT INTO pessoas (cod, nome, altura) VALUES (?, ?, ?)", cad_pessoas)
    except sqlite3.Error as erro:
        print("\033[31m[ERRO] Falha ao fazer cadastro em massa\033[m")

def cadastrar_pessoa() -> bool:
    print("\n ==== NOVO CADASTRO DE PESSOA ==== ")

    # Leitura e Validação dos dados;
    val_nome = input("Nome: ").strip()
    if not val_nome:
        print("\033[31m[ERRO] O nome é um campo obrigatório!\033[m")
        return False

    val_altura = input("Altura (metros): ").strip().replace(",", ".")
    if not val_altura:
        print("\033[31m[ERRO] A altura é um campo obrigatório!\033[m")
        return False

    try:
        altura = float(val_altura)
        if altura <= 0.30 or altura > 3.0:
            print("\033[31m[ERRO] Valor incoerente para altura!\033[m")
            return False
    except ValueError:
        print("\033[31m[ERRO] A altura precisa ser um número.\033[m")
        return False

    # Cadastro no Banco de Dados;
    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO pessoas (nome, altura) VALUES (?, ?)", (val_nome, val_altura))
            print(f"\033[32mCadastro de {val_nome} realizado com sucesso!\033[m")
            return True
    except sqlite3.Error as erro:
        print(f"\033[31m[ERRO] Falha no cadastro do banco: {erro}\033[m")
        return False

def listar_pessoas() -> bool:
    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cursor = db.cursor()
            cursor.execute("SELECT cod, nome, altura FROM pessoas ORDER BY nome;")
            primeiro = cursor.fetchone()
            if not primeiro:
                print(f"\n\033[33m[AVISO] Nenhuma pessoa foi cadastrada até agora.\033[m")
                return True

            print(f"\n"+"="*45)
            print(f"{'CÓD':<6} {'NOME':<28} {'ALTURA':>8}")
            print(f"-"*45)

            vCod, vNome, vAltura = primeiro
            print(f"{vCod:<6} {vNome:<28} {vAltura:>8}m")

            for vCod, vNome, vAltura in cursor:
                print(f"{vCod:<6} {vNome:<28} {vAltura:>8}m")

            print(f"\n" + "=" * 45)
            return True
    except sqlite3.Error as erro:
        print(f"\033[31m[ERRO] Falha ao acessar o banco: {erro}\033[m")
        return False

def atualizar_pessoa() -> bool:
    print(f"--- ATUALIZAÇÃO DE PESSOAS ---")

    listar_pessoas()

    entradaCod = input(f"informe o código da pessoa a atualizar: ").strip()
    if not entradaCod.isdigit():
        print("\033[31m[ERRO] Código inválido\033[m")
        return False

    valorCod = int(entradaCod)

    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cursor = db.cursor()
            cursor.execute("SELECT nome, altura FROM pessoas WHERE cod = ?;", (valorCod,))
            pessoa = cursor.fetchone()

            if not pessoa:
                print(f"\033[31m[ERRO] Pessoa com código {valorCod} não encontrada.\033[m")
                return False

            valorNome, valorAltura = pessoa

            print(f"\nEncontrei o registro {valorNome} com {valorAltura}m de altura.")

            conf = input("Tem certeza que deseja atualizar? [S/N] ").strip().upper()

            if conf != "S":
                print("\033[33m[AVISO] Atualização foi cancelada.\033[m")
                return True

            novoNome = input("Alterar nome: ").strip()
            novaAltura = input("Alterar altura: ").strip().replace(",", ".")

            # Mantém os valores originais caso não haja alteração
            if not novoNome:
                novoNome = valorNome

            if not novaAltura:
                novaAltura = valorAltura
            else:
                try:
                    novaAltura = float(novaAltura)

                    if novaAltura <= 0.30 or novaAltura > 3.0:
                        print("\033[31m[ERRO] Valor incoerente para altura!\033[m")
                        return False

                except ValueError:
                    print("\033[31m[ERRO] A altura precisa ser um número.\033[m")
                    return False

            cursor.execute("UPDATE pessoas SET nome = ?, altura = ? WHERE cod = ?;",
                           (novoNome, novaAltura, valorCod,))
            print(f"\033[33m[AVISO] Dados de {valorNome} foram atualizados\033[m")
            return True

    except sqlite3.Error as erro:
        print(f"\033[31m[ERRO] Falha ao atualizar: {erro}\033[m")
        return False

def excluir_pessoa() -> bool:
    print(f"--- EXCLUSÃO DE PESSOAS ---")

    listar_pessoas()

    entradaCod = input(f"informe o código da pessoa a excluir: ").strip()
    if not entradaCod.isdigit():
        print("\033[31m[ERRO] Código inválido\033[m")
        return False

    valorCod = int(entradaCod)

    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cursor = db.cursor()
            cursor.execute("SELECT nome, altura FROM pessoas WHERE cod = ?;", (valorCod,))
            pessoa = cursor.fetchone()

            if not pessoa:
                print(f"\033[31m[ERRO] Pessoa com código {valorCod} não encontrada.\033[m")
                return False

            valorNome, valorAltura = pessoa

            print(f"\nEncontrei o registro {valorNome} com {valorAltura:.2f}m de altura.")

            conf = input("Tem certeza que deseja excluir? [S/N] ").strip().upper()

            if conf != "S":
                print("\033[33m[AVISO] Exclusão foi cancelada.\033[m")
                return True

            cursor.execute("DELETE FROM pessoas WHERE cod = ?;", (valorCod,))
            print(f"\033[33m[AVISO] Acabei de excluir os dados de {valorNome}\033[m")
            return True

    except sqlite3.Error as erro:
        print(f"\033[31m[ERRO] Falha ao excluir: {erro}\033[m")
        return False

def buscar_pessoa_por_nome() -> bool:
    print("\n --- BUSCA DE PESSOA POR NOME ---")

    termo = input("Digite o nome (ou parte dele) para buscar: ")

    if not termo:
        print("\n\033[33m[AVISO] Nenhum termo foi informado!\033[m")
        return False

    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cursor = db.cursor()
            cursor.execute("SELECT cod, nome, altura FROM pessoas WHERE nome LIKE ? ORDER BY nome;", (f"%{termo}%",))

            primeiro = cursor.fetchone()
            if not primeiro:
                print(f"\n\033[33m[AVISO] Nenhuma pessoa foi encontrada com \"{termo}\"!\033[m")
                return True

            print(f"\n" + "=" * 45)
            print(f"{'CÓD':<6} {'NOME':<28} {'ALTURA':>8}")
            print(f"-" * 45)

            vCod, vNome, vAltura = primeiro
            print(f"{vCod:<6} {vNome:<28} {vAltura:>8}m")

            for vCod, vNome, vAltura in cursor:
                print(f"{vCod:<6} {vNome:<28} {vAltura:>8}m")

            print(f"\n" + "=" * 45)

            return True
    except sqlite3.Error as erro:
        print(f"[ERRO] Falha ao buscar no banco: {erro}")
        return False