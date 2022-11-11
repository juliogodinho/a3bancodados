import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.holerite import Holerite
from model.empresa import Empresa
from model.funcionario import Funcionario

from controller.controller_funcionario import Controller_Funcionario
from controller.controller_empresa import Controller_Empresa

from conexion.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Holerite:
    def __init__(self):
        self.ctrl_funcionario = Controller_Funcionario()
        self.ctrl_empresa = Controller_Empresa()
        self.relatorio = Relatorio()       
        self.mongo = MongoQueries()
        
    def inserir_holerite(self) -> Holerite:
        # Cria uma nova conexão com o banco
        opcao = "1"
        while opcao == "1":
            self.mongo.connect()
            
            # Lista os clientes existentes para inserir no pedido
            self.relatorio.get_relatorio_funcionario()
            cpf = str(input("Digite o número do CPF do Funcionario: "))
            funcionario = self.valida_funcionario(cpf)
            if funcionario == None:
                return None

            # Lista as empresas existentes para inserir na holerite
            self.relatorio.get_relatorio_empresa()
            cnpj = str(input("Digite o número do CNPJ da Empresa: "))
            empresa = self.valida_empresa(cnpj)
            if empresa == None:
                return None

            codigo = input("Codigo:")
            salariobruto = input("Salario Bruto (Novo): ")
            fgts = input("FGTS (Novo): ")
            irpf = input("irpf(Novo): ")
            salarioliquido = input("Salario Liquido (Novo): ")
            # Insere e persiste o novo cliente
            self.mongo.db["holerite"].insert_one({"codigo": codigo, "cpf": cpf, "cnpj": cnpj, "salariobruto": salariobruto, "fgts": fgts, "irpf": irpf, "salarioliquido": salarioliquido})

            #data_hoje = datetime.today().strftime("%m-%d-%Y")
            #proximo_pedido = self.mongo.db["pedidos"].aggregate([
            #                                                    {
            #                                                        '$group': {
            #                                                            '_id': '$pedidos', 
            #                                                            'proximo_pedido': {
            #                                                                '$max': '$codigo_pedido'
            #                                                            }
            #                                                        }
            #                                                    }, {
            #                                                        '$project': {
            #                                                            'proximo_pedido': {
            #                                                                '$sum': [
            #                                                                    '$proximo_pedido', 1
            #                                                                ]
            #                                                            }, 
            #                                                            '_id': 0
            #                                                        }
            #                                                    }
            #                                                ])

            #proximo_pedido = int(list(proximo_pedido)[0]['proximo_pedido'])
            # Cria um dicionário para mapear as variáveis de entrada e saída
            #data = dict(codigo_pedido=proximo_pedido, data_pedido=data_hoje, cpf=cliente.get_CPF(), cnpj=fornecedor.get_CNPJ())
            # Insere e Recupera o código do novo pedido
            #id_pedido = self.mongo.db["pedidos"].insert_one(data)
            # Recupera os dados do novo produto criado transformando em um DataFrame
            #df_pedido = self.recupera_pedido(id_pedido.inserted_id)
            # Cria um novo objeto Produto
            #novo_pedido = Pedido(df_pedido.codigo_pedido.values[0], df_pedido.data_pedido.values[0], cliente, fornecedor)
            # Exibe os atributos do novo produto
            #print(novo_pedido.to_string())
            self.mongo.close()
            opcao = input("Deseja inserir mais holerites? 1-sim 2-não")
            # Retorna o objeto novo_pedido para utilização posterior, caso necessário
            #return novo_pedido

    def atualizar_holerite(self) -> Holerite:
        # Cria uma nova conexão com o banco que permite alteração
        opcao = "1"
        while opcao == "1":
            self.mongo.connect()

            # Solicita ao usuário o código do produto a ser alterado
            codigo = int(input("Código da Holerite que irá alterar: "))        
            salariobruto = input("Salario Bruto (Novo): ")
            fgts = input("FGTS (Novo): ")
            irpf = input("irpf(Novo): ")
            salarioliquido = input("Salario Liquido (Novo): ")

            # Verifica se o produto existe na base de dados
            if not self.verifica_existencia_holerite(codigo):

                # Lista os clientes existentes para inserir no pedido
                self.relatorio.get_relatorio_funcionario()
                cpf = str(input("Digite o número do CPF do Funcionario: "))
                funcionario = self.valida_funcionario(cpf)
                if funcionario == None:
                    return None

                # Lista os fornecedores existentes para inserir no pedido
                self.relatorio.get_relatorio_empresa()
                cnpj = str(input("Digite o número do CNPJ da Empresa: "))
                empresa = self.valida_empresa(cnpj)
                if empresa == None:
                    return None

                self.mongo.db["holerite"].update_one({"codigo": f"{codigo}"}, {"$set": {"cpf": cpf, "cnpj": cnpj, "salariobruto": salariobruto, "fgts": fgts, "irpf": irpf, "salarioliquido": salarioliquido }})
                # Recupera os dados do novo cliente criado transformando em um DataFrame
                #df_holerite = self.recupera_holerite(cpf)
                #data_hoje = datetime.today().strftime("%m-%d-%Y")

                # Atualiza a descrição do produto existente
                #self.mongo.db["pedidos"].update_one({"codigo_pedido": codigo_pedido}, 
                #                                    {"$set": {"cnpj": f'{fornecedor.get_CNPJ()}',
                #                                              "cpf":  f'{cliente.get_CPF()}',
                #                                              "data_pedido": data_hoje
                #                                              }
                #                                    })
                # Recupera os dados do novo produto criado transformando em um DataFrame
                #df_pedido = self.recupera_pedido_codigo(codigo_pedido)
                # Cria um novo objeto Produto
                #pedido_atualizado = Pedido(df_pedido.codigo_pedido.values[0], df_pedido.data_pedido.values[0], cliente, fornecedor)
                # Exibe os atributos do novo produto
                #print(pedido_atualizado.to_string())
                self.mongo.close()
                opcao = input("Deseja atualizar mais holerites? 1-sim 2-não")
                # Retorna o objeto pedido_atualizado para utilização posterior, caso necessário
                #return pedido_atualizado
            else:
                self.mongo.close()
                opcao = "2"
                print(f"O código {codigo} não existe.")
                return None

    def excluir_holerite(self):
        # Cria uma nova conexão com o banco que permite alteração
        opcao = "1"
        while opcao == "1":
            self.mongo.connect()

            # Solicita ao usuário o código do produto a ser alterado
            codigo = int(input("Código da Holerite que irá excluir: "))        
            # Verifica se o produto existe na base de dados
            if not self.verifica_existencia_holerite(codigo):            
                # Recupera os dados do novo produto criado transformando em um DataFrame
                #df_holerite = self.recupera_holerite_codigo(codigo)
                #funcionario = self.valida_funcionario(df_holerite.cpf.values[0])
                #fornecedor = self.valida_fornecedor(df_pedido.cnpj.values[0])
                
                opcao_excluir = input(f"Tem certeza que deseja excluir a holerite {codigo} [1-sim 2-nao]: ")
                if opcao_excluir == "1":
                    #print("Atenção, caso o pedido possua itens, também serão excluídos!")
                    #opcao_excluir = input(f"Tem certeza que deseja excluir o pedido {codigo_pedido} [S ou N]: ")
                    #if opcao_excluir.lower() == "s":
                        # Revome o produto da tabela
                    self.mongo.db["holerite"].delete_one({"codigo":f"{codigo}"})
                    #print("Itens do pedido removidos com sucesso!")
                    #self.mongo.db["pedidos"].delete_one({"codigo_pedido": codigo_pedido})
                    # Cria um novo objeto Produto para informar que foi removido
                    #pedido_excluido = Pedido(df_pedido.codigo_pedido.values[0], df_pedido.data_pedido.values[0], cliente, fornecedor)
                    self.mongo.close()
                    # Exibe os atributos do produto excluído
                    print("Holerite Removida com Sucesso!")
                    opcao = input("Deseja excluir mais holerites? 1-sim 2-não")
                    #print(pedido_excluido.to_string())
            else:
                self.mongo.close()
                opcao = "2"
                print(f"O código {codigo} não existe.")

    def verifica_existencia_holerite(self, codigo:str=None, external: bool = False) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_holerite = pd.DataFrame(self.mongo.db["holerite"].find({"codigo":f"{codigo}"}, {"codigo": 1, "cpf": 1, "cnpj": 1, "salariobruto": 1, "fgts": 1, "irpf": 1, "salarioliquido": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_holerite.empty

    def recupera_holerite(self, _id:ObjectId=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_holerite = pd.DataFrame(list(self.mongo.db["holerite"].find({"_id":_id}, {"codigo": 1, "cpf": 1, "cnpj": 1, "salariobruto": 1, "fgts": 1, "irpf": 1, "salarioliquido": 1, "_id": 0})))
        return df_holerite

    def recupera_holerite_codigo(self, codigo:int=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_holerite = pd.DataFrame(list(self.mongo.db["holerite"].find({"codigo": codigo}, {"codigo": 1, "cpf": 1, "cnpj": 1, "salariobruto": 1, "fgts": 1, "irpf": 1, "salarioliquido": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_holerite

    def valida_funcionario(self, cpf:str=None) -> Funcionario:
        if self.ctrl_funcionario.verifica_existencia_funcionario(cpf=cpf, external=True):
            print(f"O CPF {cpf} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_funcionario = self.ctrl_funcionario.recupera_funcionario(cpf=cpf, external=True)
            # Cria um novo objeto cliente
            funcionario = Funcionario(df_funcionario.cpf.values[0], df_funcionario.nome.values[0])
            return funcionario

    def valida_empresa(self, cnpj:str=None) -> Empresa:
        if self.ctrl_empresa.verifica_existencia_empresa(cnpj, external=True):
            print(f"O CNPJ {cnpj} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo fornecedor criado transformando em um DataFrame
            df_empresa = self.ctrl_empresa.recupera_empresa(cnpj, external=True)
            # Cria um novo objeto fornecedor
            empresa = Empresa(df_empresa.cnpj.values[0], df_empresa.razaosocial.values[0], df_empresa.nomefantasia.values[0])
            return empresa