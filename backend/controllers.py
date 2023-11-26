# controllers.py
import pika
import psycopg2

# Controller - Veiculo
class VeiculoController:
    def __init__(self, model):
        self.model = model

    def cadastrar_veiculo(self, tipo, marca, modelo, ano, placa):
        sucesso = self.model.cadastrar_veiculo(tipo, marca, modelo, ano, placa)
        if sucesso:
            self.enviar_mensagem(tipo, marca, modelo, ano, placa)

    def enviar_mensagem(self, tipo, marca, modelo, ano, placa):
        mensagem = f"{tipo};{marca};{modelo};{ano};{placa}"
        try:
            credentials = pika.PlainCredentials('admin', '1234')
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
            channel = connection.channel()
            channel.basic_publish(exchange='', routing_key='fila_veiculos', body=mensagem)
            print(f'Mensagem enviada: {mensagem}')
            connection.close()
        except Exception as e:
            print(f"Ocorreu um erro ao conectar-se ao RabbitMQ: {e}")

# Controller - Cartao
class CartaoController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def cadastrar_cartao(self, cliente_id, tipo, numero):
        if self.model.cadastrar_cartao(cliente_id, tipo, numero):
            self.view.mostrar_mensagem("Cartão cadastrado com sucesso!")
            self.model.enviar_resposta_para_cliente(cliente_id, "RESPOSTA_CADASTRO_CARTAO;SUCESSO")
        else:
            self.view.mostrar_mensagem("Erro ao cadastrar o cartão.")
            self.model.enviar_resposta_para_cliente(cliente_id, "RESPOSTA_CADASTRO_CARTAO;ERRO")

# Controller - Cliente
class ClienteController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def atualizar_cliente(self, cliente_id, novo_nome, novo_telefone):
        self.model.atualizar_cliente(cliente_id, novo_nome, novo_telefone)
        mensagem = f'Dados do Cliente {cliente_id} atualizados com sucesso.'
        self.view.mostrar_mensagem(mensagem)

# Controller - Entregador
class EntregadorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def atualizar_entregador(self, entregador_id, novo_nome, novo_telefone):
        self.model.atualizar_entregador(entregador_id, novo_nome, novo_telefone)
        mensagem = f'Dados do Entregador {entregador_id} atualizados com sucesso.'
        self.view.mostrar_mensagem(mensagem)

# Controller - Usuario
class UsuarioController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def realizar_login(self, cpf, senha):
        nome_usuario = self.model.fazer_login(cpf, senha)
        if nome_usuario:
            self.view.mostrar_mensagem(f"Bem-vindo, {nome_usuario}!")

    def realizar_logout(self):
        sucesso = self.model.fazer_logout()
        if sucesso:
            self.view.mostrar_mensagem("Logout bem-sucedido!")
        else:
            self.view.mostrar_mensagem("Falha ao fazer logout.")
