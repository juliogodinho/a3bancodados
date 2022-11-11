import pandas as pd
from model.empresa import Empresa
from conexion.mongo_queries import MongoQueries

class Controller_Empresa:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_empresa(self) -> Empresa:
        # Cria uma nova conexão com o banco que permite alteração
        opcao = "1"
        while opcao == "1":
            self.mongo.connect()
            # Solicita ao usuario o novo CPF
            cnpj = input("CNPJ (Novo): ")

            if self.verifica_existencia_empresa(cnpj):
                # Solicita ao usuario o novo nome
                nomefantasia = input("Nome Fantasia (Novo): ")
                razaosocial = input("Razao Social (Novo): ")
                # Insere e persiste o novo cliente
                self.mongo.db["empresa"].insert_one({"cnpj": cnpj, "nomefantasia": nomefantasia, "razaosocial": razaosocial})
                # Recupera os dados do novo cliente criado transformando em um DataFrame
                df_empresa = self.recupera_empresa(cnpj)
                # Cria um novo objeto Cliente
                #novo_empresa = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0])
                # Exibe os atributos do novo cliente
                #print(novo_cliente.to_string())
                self.mongo.close()
                opcao = input("deseja inserir mais empresas 1-sim 2-não")
                # Retorna o objeto novo_cliente para utilização posterior, caso necessário
                #return novo_cliente
            else:
                self.mongo.close()
                print(f"O CNPJ {cnpj} já está cadastrado.")
                opcao = "2"
                return None

    def atualizar_empresa(self) -> Empresa:
        # Cria uma nova conexão com o banco que permite alteração
        opcao = "1"
        while opcao == "1":
            self.mongo.connect()
            # Solicita ao usuário o código do cliente a ser alterado
            cnpj = input("CNPJ da empresa que deseja alterar: ")

            # Verifica se o cliente existe na base de dados
            if not self.verifica_existencia_empresa(cnpj):
                # Solicita a nova descrição do cliente
                novo_nomefantasia = input("Nome Fantasia (Novo): ")
                novo_razaosocial = input("Razao Social (Novo): ")
                # Atualiza o nome do cliente existente
                self.mongo.db["empresa"].update_one({"cnpj": f"{cnpj}"}, {"$set": {"razaosocial":novo_razaosocial, "nomefantasia":novo_nomefantasia}})
                # Recupera os dados do novo cliente criado transformando em um DataFrame
                df_empresa = self.recupera_empresa(cnpj)
                # Cria um novo objeto cliente
                #cliente_atualizado = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0])
                # Exibe os atributos do novo cliente
                #print(cliente_atualizado.to_string())
                self.mongo.close()
                opcao = input("Deseja atualizar mais empresas? 1-sim 2-não")
                # Retorna o objeto cliente_atualizado para utilização posterior, caso necessário
                #return cliente_atualizado
            else:
                self.mongo.close()
                print(f"O CNPJ {cnpj} não existe.")
                opcao = "2"
                return None

    def excluir_empresa(self):
        # Cria uma nova conexão com o banco que permite alteração
        opcao = "1"
        while opcao == "1":
            self.mongo.connect()
            # Solicita ao usuário o CPF do Cliente a ser alterado
            cnpj = input("CNPJ da Empresa que irá excluir: ")
            confirma = input("Tem certeza que deseja excluir? 1-sim 2-não")
            if confirma == "1":
                # Verifica se o cliente existe na base de dados
                if not self.verifica_existencia_empresa(cnpj):            
                    # Recupera os dados do novo cliente criado transformando em um DataFrame
                    df_empresa = self.recupera_empresa(cnpj)
                    # Revome o cliente da tabela
                    self.mongo.db["empresa"].delete_one({"cnpj":f"{cnpj}"})
                    # Cria um novo objeto Cliente para informar que foi removido
                    #empresa_excluido = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0])
                    self.mongo.close()
                    print("Empresa Removida com Sucesso!")
                    opcao = input("Deseja excluir mais empresas? 1-sim 2-não")
                    # Exibe os atributos do cliente excluído
                    #print(cliente_excluido.to_string())
                else:
                    self.mongo.close()
                    opcao = "2"
                    print(f"O CNPJ {cnpj} não existe.")
            else:
                self.mongo.close()
                opcao = input("Deseja excluir mais empresas? 1-sim 2-não")

    def verifica_existencia_empresa(self, cnpj:str=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_empresa = pd.DataFrame(self.mongo.db["empresa"].find({"cnpj":f"{cnpj}"}, {"cnpj": 1, "nomefantasia": 1, "razaosocial":1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_empresa.empty

    def recupera_empresa(self, cnpj:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_empresa = pd.DataFrame(list(self.mongo.db["empresa"].find({"cnpj":f"{cnpj}"}, {"cnpj": 1, "nomefantasia": 1, "razaosocial":1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_empresa