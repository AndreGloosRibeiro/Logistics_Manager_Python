from collections import defaultdict
import random
import string
import uuid


class Produto:
    def __init__(self, codigo, nome, peso, preco):
        self.codigo = codigo
        self.nome = nome
        self.peso = peso
        self.preco = preco


class Pedido:
    def __init__(self, produtos, codigo_rastreio):
        self.codigo = str(uuid.uuid4())[:5]  # Gera um código de 5 caracteres
        self.produtos = produtos
        self.status = "Pendente"
        self.codigo_rastreio = (
            codigo_rastreio  # Associar código de rastreamento ao pedido
        )

    def calcular_peso_total(self):
        peso_total = sum(produto.peso for produto in self.produtos)
        return peso_total

    def calcular_valor_total(self):
        valor_total = sum(produto.preco for produto in self.produtos)
        return valor_total

    def atualizar_status(self, novo_status):
        self.status = novo_status

    def obter_status(self):
        return self.status


class Cliente:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco


class Entrega:
    def __init__(self, pedido, cliente, metodo_entrega):
        self.pedido = pedido
        self.cliente = cliente
        self.metodo_entrega = metodo_entrega


class Armazem:
    def __init__(self):
        self.produtos = {}

    def adicionar_produto(self, produto):
        if produto.codigo not in self.produtos:
            self.produtos[produto.codigo] = produto
            print(f"Produto {produto.nome} adicionado ao armazém.")
        else:
            print("Produto já existe no armazém.")

    def remover_produto(self, codigo_produto):
        if codigo_produto in self.produtos:
            del self.produtos[codigo_produto]
            print("Produto removido do armazém.")
        else:
            print("Produto não encontrado no armazém.")

    def listar_produtos(self):
        print("Produtos no armazém:")
        for produto in self.produtos.values():
            print(
                f"- {produto.nome} (Código: {produto.codigo}, Peso: {produto.peso}, Preço: R${produto.preco})"
            )

    def encontrar_produto(self, codigo_produto):
        return self.produtos.get(codigo_produto)


class SistemaLogistico:
    def __init__(self):
        self.armazem = Armazem()
        self.clientes = []
        self.pedidos = []

    def fazer_pedido(self, cliente, codigos_produtos):
        produtos_pedido = []
        for codigo_produto in codigos_produtos:
            produto = self.armazem.encontrar_produto(codigo_produto)
            if produto:
                produtos_pedido.append(produto)
            else:
                print(f"Produto com código {codigo_produto} não encontrado no armazém.")
                return

        codigo_rastreio = self.gerar_codigo_rastreio()  # Gerar código de rastreamento
        pedido = Pedido(produtos_pedido, codigo_rastreio)
        entrega = Entrega(pedido, cliente, "normal")
        self.pedidos.append((pedido, cliente, entrega))
        print(f"Pedido realizado com sucesso! Código de rastreio: {codigo_rastreio}")

    def gerar_codigo_rastreio(self):
        caracteres = string.ascii_letters + string.digits
        codigo = "".join(random.choices(caracteres, k=5))
        return codigo

    def processar_pagamento(self, pedido):
        valor_total = pedido.calcular_valor_total()
        # Processamento de pagamento
        print(f"Processando pagamento no valor de R${valor_total}...")
        print("Pagamento processado com sucesso!")

    def rastrear_pedido(self, codigo_pedido):
        for pedido, _, _ in self.pedidos:
            if (
                pedido.codigo_rastreio == codigo_pedido
            ):  # Verificar pelo código de rastreamento
                status_atual = pedido.obter_status()
                print(f"Status atual do pedido {pedido.codigo}: {status_atual}")
                return
        print("Pedido não encontrado.")

    def atualizar_status_pedido(self, codigo_pedido, novo_status):
        for pedido, _, _ in self.pedidos:
            if (
                pedido.codigo_rastreio == codigo_pedido
            ):  # Verificar pelo código de rastreamento
                pedido.atualizar_status(novo_status)
                print("Status do pedido atualizado com sucesso.")
                return
        print("Pedido não encontrado.")

    def gerar_relatorio_vendas(self, periodo):
        vendas_por_produto = defaultdict(int)

        for pedido, _, _ in self.pedidos:
            if pedido.data == periodo:
                for produto in pedido.produtos:
                    vendas_por_produto[produto.nome] += 1

        print(f"Relatório de vendas para o período {periodo}:")
        for produto, quantidade_vendida in vendas_por_produto.items():
            print(f"{produto}: {quantidade_vendida} unidades")


# Função para exibir o menu principal
def exibir_menu_principal():
    print("\n===== Menu Principal =====")
    print("1. Adicionar produto ao armazém")
    print("2. Remover produto do armazém")
    print("3. Listar produtos do armazém")
    print("4. Fazer um pedido")
    print("5. Rastrear um pedido")
    print("6. Atualizar status do pedido")
    print("7. Gerar relatório de vendas")
    print("8. Sair")


# Função para fazer um pedido
def fazer_pedido():
    nome_cliente = input("Digite o nome do cliente: ")
    endereco_cliente = input("Digite o endereço do cliente: ")

    codigos_produtos = []
    while True:
        codigo_produto = input("Digite o código do produto (ou 'fim' para terminar): ")
        if codigo_produto == "fim":
            break
        else:
            codigos_produtos.append(codigo_produto)

    cliente = Cliente(nome_cliente, endereco_cliente)
    sistema.fazer_pedido(cliente, codigos_produtos)


# Função para rastrear um pedido
def rastrear_pedido():
    codigo_pedido = input("Digite o código de rastreamento do pedido: ")
    sistema.rastrear_pedido(codigo_pedido)


# Função para atualizar o status de um pedido
def atualizar_status_pedido():
    codigo_pedido = input("Digite o código de rastreamento do pedido: ")
    novo_status = input("Digite o novo status do pedido: ")
    sistema.atualizar_status_pedido(codigo_pedido, novo_status)


# Função para solicitar o relatório de vendas
def solicitar_relatorio_vendas():
    periodo = input("Digite o período para o relatório de vendas: ")
    sistema.gerar_relatorio_vendas(periodo)


# Exemplo de uso
if __name__ == "__main__":
    sistema = SistemaLogistico()

    while True:
        exibir_menu_principal()
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            codigo = input("Digite o código do produto: ")
            nome = input("Digite o nome do produto: ")
            peso = float(input("Digite o peso do produto: "))
            preco = float(input("Digite o preço do produto: "))
            produto = Produto(codigo, nome, peso, preco)
            sistema.armazem.adicionar_produto(produto)
        elif escolha == "2":
            codigo = input("Digite o código do produto a ser removido: ")
            sistema.armazem.remover_produto(codigo)
        elif escolha == "3":
            sistema.armazem.listar_produtos()
        elif escolha == "4":
            fazer_pedido()
        elif escolha == "5":
            rastrear_pedido()
        elif escolha == "6":
            atualizar_status_pedido()
        elif escolha == "7":
            solicitar_relatorio_vendas()
        elif escolha == "8":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
