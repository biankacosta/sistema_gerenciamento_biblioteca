import json
import random
import string
from enum import IntEnum, unique


@unique
class Telas(IntEnum):
    TELA_INICIAL = 0
    TELA_LISTA = 1
    TELA_CONSULTA_LIVRO = 2
    TELA_EMPRESTIMO = 3
    TELA_PROCURAR_LIVRO = 4


class Sistema:

    def __init__(self):
        self.tela_atual = Telas.TELA_INICIAL
        self.mudar_de_tela()

    def ler_json(self, nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
        return dados

    def atualizar_json(self, arr, nome_arquivo):
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(arr, arquivo, indent=4)

    def gerar_id_aleatorio(self):
        livros = self.ler_json('livros_bd.json')
        self.lista_ids = [livro['id'] for livro in livros]

        while True:
            letra = random.choice(string.ascii_uppercase)
            numeros = ''.join(random.choice(string.digits) for _ in range(2))
            id_aleatorio = letra + numeros

            if id_aleatorio not in self.lista_ids:
                return id_aleatorio

    def cadastrar_livro(self):
        novo_livro = {'nome': input("\nDigite o nome do livro: "),
                      'autor': input("Digite o nome do autor: "),
                      'ano': input("Digite o ano de publicação: "),
                      'num_pags': input("Digite o número de páginas: "),
                      'editora': input("Digite o nome da editora: "),
                      'estado': "Disponivel",
                      'id': self.gerar_id_aleatorio()}

        livros = self.ler_json('livros_bd.json')
        livros.append(novo_livro)
        self.atualizar_json(livros, 'livros_bd.json')
        print("Livro cadastrado com sucesso!\n")

    def cadastrar_usuario(self):
        print("Cadastro de Usuário...")
        novo_usuario = {'nome': input("\nDigite o nome do usuário: "),
                        'cpf': input("Digite o CPF do usuário: "),
                        'telefone': input("Digite o telefone do usuário: "),
                        'emprestimo': "Nao",
                        "livro": "",
                        "id_livro": ""}

        usuarios = self.ler_json('usuarios_bd.json')
        usuarios.append(novo_usuario)
        self.atualizar_json(usuarios, 'usuarios_bd.json')
        print("Usuário cadastrado com sucesso!\n")

    def cadastro_emprestimo(self):
        livros = self.ler_json('livros_bd.json')
        usuarios = self.ler_json('usuarios_bd.json')
        nome_livro = self.livro_encontrado["nome"]
        id_livro = self.livro_encontrado['id']
        livros[self.resultado_busca]['estado'] = 'Indisponível'
        usuarios[self.resultado_busca_cpf]['livro'] = nome_livro
        usuarios[self.resultado_busca_cpf]['emprestimo'] = 'Sim'
        usuarios[self.resultado_busca_cpf]['id_livro'] = id_livro
        self.atualizar_json(livros, 'livros_bd.json')
        self.atualizar_json(usuarios, 'usuarios_bd.json')
        print("Empréstimo realizado com sucesso!")

    def lista_usuario(self):
        usuarios = self.ler_json('usuarios_bd.json')
        for usuario in usuarios:
            print(f'''
                        Nome: {usuario['nome']}
                        CPF: {usuario['cpf']}
                        Telefone: {usuario['telefone']}
                        Empréstimo Ativo: {usuario['emprestimo']} 
                        -----------------''')

    def lista_de_livros(self):
        livros = self.ler_json('livros_bd.json')
        for livro in livros:
            print(f'''
                {livro['nome']}
                Autor: {livro['autor']}
                Editora: {livro['editora']}
                ID: {livro['id']} 
                -----------------''')

    def consultar_livro(self):
        id_busca = input("Digite o ID do livro que deseja consultar: ")
        self.resultado_consultar_livro = 0

        self.ordenar_infos("id", 'livros_bd.json')
        livros = self.ler_json('livros_bd.json')
        self.resultado_busca = self.pesquisa_binaria(livros, 'id', id_busca)
        if self.resultado_busca != "Elemento nao encontrado":
            self.livro_encontrado = livros[self.resultado_busca]
            print(livros[self.resultado_busca]['nome'])
            self.info_livro(self.livro_encontrado)
            self.resultado_consultar_livro = 1
        else:
            print(f"Não foi encontrado nenhum livro com o ID {id_busca}.")

        return self.resultado_consultar_livro

    def consultar_cpf(self):
        cpf_busca = input("Digite o CPF do usuário: ")
        self.resultado_consultar_cpf = 0

        self.ordenar_infos("cpf", 'usuarios_bd.json')
        self.usuarios = self.ler_json('usuarios_bd.json')
        self.resultado_busca_cpf = self.pesquisa_binaria(self.usuarios, 'cpf', cpf_busca)
        if self.resultado_busca_cpf != "Elemento nao encontrado":
            if self.usuarios[self.resultado_busca_cpf]['emprestimo'] == 'Sim':
                self.resultado_consultar_cpf = 1
            else:
                self.resultado_consultar_cpf = 2
        else:
            print(f"Não foi encontrado nenhum CPF com o número {cpf_busca}.")

        return self.resultado_consultar_cpf

    def procurar_livro(self, opcao):
        print(opcao)

        valor_pesquisa = input("Digite o que deseja procurar: ")

        if opcao == "1":
            atributo_pesquisa = "nome"
        elif opcao == "2":
            atributo_pesquisa = "autor"
        else:
            atributo_pesquisa = "editora"

        livros = self.ler_json('livros_bd.json')
        for livro in livros:
            if livro[atributo_pesquisa] == valor_pesquisa:
                self.info_livro(livro)

        print(f"O resultado '{valor_pesquisa}' não foi encontrado na propriedade de pesquisa escolhida.")

    def devolver_livro(self):
        print("Devolução de livro. Digite o CPF vinculado ao empréstimo.")

        if self.consultar_cpf() == 1:
            print(f"Usuário: {self.usuarios[self.resultado_busca_cpf]['nome']}")
            self.realizar_devolucao()
        elif self.consultar_cpf() == 2:
            print(f"O usuário {self.usuarios[self.resultado_busca_cpf]['nome']} digitado não tem empréstimos ativos.")

    def realizar_devolucao(self):
        livros = self.ler_json('livros_bd.json')
        usuarios = self.ler_json('usuarios_bd.json')

        id_livro_emprestado = usuarios[self.resultado_busca_cpf]['id_livro']
        print(f"ID livro emprestado: {id_livro_emprestado}. Por favor, digite este ID no campo abaixo.")
        if self.consultar_livro() == 1:
            livros[self.resultado_busca]['estado'] = 'Disponivel'

        usuarios[self.resultado_busca_cpf]['livro'] = ""
        usuarios[self.resultado_busca_cpf]['emprestimo'] = 'Nao'
        usuarios[self.resultado_busca_cpf]['id_livro'] = ""
        self.atualizar_json(livros, 'livros_bd.json')
        self.atualizar_json(usuarios, 'usuarios_bd.json')
        print(f"Devolução realizada!")

    def deletar_livro(self):
        livros = self.ler_json('livros_bd.json')
        livro = self.resultado_busca
        livro_deletar = livros.pop(livro)
        self.atualizar_json(livros, 'livros_bd.json')
        print(f"O livro '{livro_deletar['nome']}' foi excluído com sucesso.")


    def historico_de_emprestimo(self):
        usuarios = self.ler_json('usuarios_bd.json')
        for usuario in usuarios:
            if usuario['emprestimo'] == 'Sim':
                self.info_usuario(usuario)

    def verifica_livro_disponivel(self):
        if self.livro_encontrado['estado'] == 'Indisponível':
            print('\n O livro está indisponível')
        else:
            self.gerenciador_consultar_cpf()

    def gerenciador_consultar_cpf(self):
        resultado_consultar_cpf = self.consultar_cpf()
        if resultado_consultar_cpf == 1:
            print("Esse usuário está com o emprestimo indisponivel")
        elif resultado_consultar_cpf == 2:
            self.cpf_encontrado = self.usuarios[self.resultado_busca_cpf]
            self.info_usuario(self.cpf_encontrado)
            self.cadastro_emprestimo()
        elif resultado_consultar_cpf == 0:
            print("Para cadastrar esse usuário, vá para a tela inicial")


    def ordenar_infos(self, ordem, nome_arquivo):
        infos = self.ler_json(nome_arquivo)
        self.quick_sort(infos, ordem, 0, len(infos) - 1)
        self.atualizar_json(infos, nome_arquivo)

    def info_usuario(self, usuario):
        return print(f'''
                        Nome: {usuario['nome']}
                        CPF: {usuario['cpf']}
                        Telefone: {usuario['telefone']}
                        Empréstimo Ativo: {usuario['emprestimo']} 
                        Livro: {usuario['livro']}
                        ID do livro: {usuario['id_livro']}
                        -----------------''')

    def info_livro(self, livro):
        return print(f'''
                    Título: {livro['nome']}
                    Autor: {livro['autor']}
                    Ano: {livro['ano']}
                    Número de páginas: {livro['num_pags']}
                    Editora: {livro['editora']}
                    Status: {livro['estado']}
                    ID: {livro['id']} 
                    -----------------''')

    def partition(self, arr, elemento, low, high):
        pivot = arr[high][elemento]
        i = low - 1

        for j in range(low, high):
            if arr[j][elemento] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quick_sort(self, arr, elemento, low, high):
        if low < high:
            pivot_index = self.partition(arr, elemento, low, high)
            self.quick_sort(arr, elemento, low, pivot_index - 1)
            self.quick_sort(arr, elemento, pivot_index + 1, high)

    def pesquisa_binaria(self, arr, elemento, target):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid][elemento] == target:
                return mid
            elif arr[mid][elemento] > target:
                right = mid - 1
            else:
                left = mid + 1
        return "Elemento nao encontrado"

    def mudar_de_tela(self):
        while True:
            # TELA INICIA-----------------------------------
            if self.tela_atual == Telas.TELA_INICIAL:
                print('')
                print("Escolha uma opção:")
                print("1. Cadastrar livro")
                print("2. Listar livros")
                print("3. Cadastrar Usuário")
                print("4. Ver lista de usuários cadastrados")
                print("5. Ver histórico de emprestimos")
                print("6. Sair do programa")
                opcao = input("Digite o número da opção desejada: ")
                if opcao == '1':
                    self.cadastrar_livro()
                elif opcao == '2':
                    self.lista_de_livros()
                    self.tela_atual = Telas.TELA_LISTA
                elif opcao == '3':
                    self.cadastrar_usuario()
                elif opcao == '4':
                    self.lista_usuario()
                elif opcao == '5':
                    self.historico_de_emprestimo()
                    self.tela_atual = Telas.TELA_EMPRESTIMO
                elif opcao == '6':
                    return print("Programa encerrado.")
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")

            # TELA LISTA-----------------------------------
            elif self.tela_atual == Telas.TELA_LISTA:
                print('')
                print("1. Consultar livro por ID")
                print("2. Procurar livro por NOME ou AUTOR ou EDITORA")
                print("3. Tela Inicial")
                opcao = input("Digite o número da opção desejada: ")
                if opcao == '1':
                    if self.consultar_livro() == 1:
                        self.tela_atual = Telas.TELA_CONSULTA_LIVRO
                elif opcao == '2':
                    self.tela_atual = Telas.TELA_PROCURAR_LIVRO
                elif opcao == '3':
                    self.tela_atual = Telas.TELA_INICIAL
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")

            # TELA CONSULTA-----------------------------------
            elif self.tela_atual == Telas.TELA_CONSULTA_LIVRO:
                print('')
                print("1. Empréstimo")
                print("2. Deletar livro")
                print("3. Voltar para a Lista de Livros")
                opcao = input("Digite o número da opção desejada: ")
                if opcao == '1':
                    self.verifica_livro_disponivel()
                    self.tela_atual = Telas.TELA_LISTA
                elif opcao == '2':
                    self.deletar_livro()
                    self.tela_atual = Telas.TELA_INICIAL
                elif opcao == '3':
                    self.tela_atual = Telas.TELA_LISTA
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")

            elif self.tela_atual == Telas.TELA_EMPRESTIMO:
                print('')
                print("1. Devolver livro")
                print("2. Voltar para a Tela Inicial")
                opcao = input("Digite o número da opção desejada: ")
                if opcao == '1':
                    self.devolver_livro()
                elif opcao == '2':
                    self.tela_atual = Telas.TELA_INICIAL
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")

            elif self.tela_atual == Telas.TELA_PROCURAR_LIVRO:
                print('')
                print('Escolha por qual propriedade você deseja pesquisar:')
                print("1. Título")
                print("2. Autor")
                print("3. Editora")
                opcao = input("Digite o número da opção desejada: ")
                if opcao == '1' or opcao == '2' or opcao == '3':
                    self.procurar_livro(opcao)
                    self.tela_atual = Telas.TELA_LISTA
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")


if __name__ == '__main__':
    s = Sistema()
