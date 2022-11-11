import pandas as pd
from model.funcionario import Funcionario
from conexion.mongo_queries import MongoQueries

class Controller_Funcionario:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_funcionario(self) -> Funcionario:
        # Cria uma nova conexão com o banco que permite alteração
        opcao = "1"
        while opcao == "1":
            self.mongo.connect()

            # Solicita ao usuario o novo CPF
            cpf = input("CPF (Novo): ")

            if self.verifica_existencia_funcionario(cpf):
                # Solicita ao usuario o novo nome
                nome = input("Nome (Novo): ")
                # Insere e persiste o novo cliente
                self.mongo.db["funcionario"].insert_one({"cpf": cpf, "nome": nome})
                # Recupera os dados do novo cliente criado transformando em um DataFrame
                df_funcionario = self.recupera_funcionario(cpf)
                # Cria um novo objeto Cliente
                novo_funcionario = Funcionario(df_funcionario.cpf.values[0], df_funcionario.nome.values[0])
                # Exibe os atributos do novo cliente
                print(novo_funcionario.to_string())
                self.mongo.close()
                opcao = input("Deseja inserir mais funcionarios? 1-sim 2-nao")
                # Retorna o objeto novo_cliente para utilização posterior, caso necessário
                #return novo_funcionario
            else:
                self.mongo.close()
                opcao = "2"
                print(f"O CPF {cpf} já está cadastrado.")
                return None

    def atualizar_funcionario(self) -> Funcionario:
        # Cria uma nova conexão com o banco que permite alteração
        opcao = "1"
        while opcao == "1":
            self.mongo.connect()

            # Solicita ao usuário o código do cliente a ser alterado
            cpf = input("CPF do funcionario que deseja alterar o nome: ")

            # Verifica se o cliente existe na base de dados
            if not self.verifica_existencia_funcionario(cpf):
                # Solicita a nova descrição do cliente
                novo_nome = input("Nome (Novo): ")
                # Atualiza o nome do cliente existente
                self.mongo.db["funcionario"].update_one({"cpf": f"{cpf}"}, {"$set": {"nome": novo_nome}})
                # Recupera os dados do novo cliente criado transformando em um DataFrame
                df_funcionario = self.recupera_funcionario(cpf)
                # Cria um novo objeto cliente
                funcionario_atualizado = Funcionario(df_funcionario.cpf.values[0], df_funcionario.nome.values[0])
                # Exibe os atributos do novo cliente
                print(funcionario_atualizado.to_string())
                self.mongo.close()
                opcao = input("Deseja atualizar mais funcionarios? 1-sim 2-não")
                # Retorna o objeto cliente_atualizado para utilização posterior, caso necessário
                #return funcionario_atualizado
            else:
                self.mongo.close()
                print(f"O CPF {cpf} não existe.")
                opcao = "2"
                return None

    def excluir_funcionario(self):
        # Cria uma nova conexão com o banco que permite alteração
        opcao = "1"
        while opcao == "1":
            self.mongo.connect()

            # Solicita ao usuário o CPF do Cliente a ser alterado
            cpf = input("CPF do Funcionario que irá excluir: ")
            confirma = input("Tem certeza que deseja excluir o funcionario? 1-sim 2-não")
            # Verifica se o cliente existe na base de dados
            if confirma == "1":
                if not self.verifica_existencia_funcionario(cpf):            
                    # Recupera os dados do novo cliente criado transformando em um DataFrame
                    df_funcionario = self.recupera_funcionario(cpf)
                    # Revome o cliente da tabela
                    self.mongo.db["funcionario"].delete_one({"cpf":f"{cpf}"})
                    # Cria um novo objeto Cliente para informar que foi removido
                    funcionario_excluido = Funcionario(df_funcionario.cpf.values[0], df_funcionario.nome.values[0])
                    self.mongo.close()
                    # Exibe os atributos do cliente excluído
                    print("Funcionario Removido com Sucesso!")
                    print(funcionario_excluido.to_string())
                    opcao = input("Deseja excluir mais funcionarios? 1-sim 2-nao")
                else:
                    self.mongo.close()
                    opcao = "2"
                    print(f"O CPF {cpf} não existe.")
            else:
                opcao = input("Deseja excluir mais funcionarios 1-sim 2-não")

    def verifica_existencia_funcionario(self, cpf:str=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_funcionario = pd.DataFrame(self.mongo.db["funcionario"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_funcionario.empty

    def recupera_funcionario(self, cpf:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_funcionario = pd.DataFrame(list(self.mongo.db["funcionario"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome": 1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_funcionario