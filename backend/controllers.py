""" Módulo pika é responsável por fazer a conexão entre rabbitMQ e o servidor """
import pika


class VeiculoController:
    """ Classe responsável pelo modelo Veículo """
    def __init__(self, model):
        self.model = model

    def cadastrar_veiculo(self, tipo, marca, modelo, ano, placa):
        """ Método responsável por fazer a inserção do carro no banco de dados """
        sucesso = self.model.cadastrar_veiculo(tipo, marca, modelo, ano, placa)
        if sucesso:
            self.enviar_mensagem(tipo, marca, modelo, ano, placa)

    def enviar_mensagem(self, tipo, marca, modelo, ano, placa):
        """ Método responsável por enviar mensagem para o rabbitMQ """
        mensagem = f"{tipo};{marca};{modelo};{ano};{placa}"
        try:
            credentials = pika.PlainCredentials('admin', '1234')
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
            port=5672, credentials=credentials))
            channel = connection.channel()
            channel.basic_publish(exchange='', routing_key='fila_veiculos', body=mensagem)
            print(f'Mensagem enviada: {mensagem}')
            connection.close()
        except pika.exceptions.AMQPError as amqp_error:
            # Lidar com erros específicos do RabbitMQ
            print(f"Erro no RabbitMQ ao enviar mensagem: {amqp_error}")

class CartaoController:
    """ Classe responsável pelo controle do Cartão """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def cadastrar_cartao(self, cliente_id, tipo, numero):
        """ Método responsável por inserir o cartão no banco de dados """
        if self.model.cadastrar_cartao(cliente_id, tipo, numero):
            self.view.mostrar_mensagem("Cartão cadastrado com sucesso!")
            self.model.enviar_resposta_para_cliente(cliente_id, "RESPOSTA_CADASTRO_CARTAO;SUCESSO")
        else:
            self.view.mostrar_mensagem("Erro ao cadastrar o cartão.")
            self.model.enviar_resposta_para_cliente(cliente_id, "RESPOSTA_CADASTRO_CARTAO;ERRO")


class ClienteController:
    """ Método responsável pelo controle do cliente """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def atualizar_cliente(self, cliente_id, novo_nome, novo_telefone):
        """ Médodo responsável por atualizar os dados do cliente """
        self.model.atualizar_cliente(cliente_id, novo_nome, novo_telefone)
        mensagem = f'Dados do Cliente {cliente_id} atualizados com sucesso.'
        self.view.mostrar_mensagem(mensagem)


class EntregadorController:
    """ Classe responsável pelo controle do Entregador """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def atualizar_entregador(self, entregador_id, novo_nome, novo_telefone):
        """ Método responsável por atualizar os dados do Entregador """
        self.model.atualizar_entregador(entregador_id, novo_nome, novo_telefone)
        mensagem = f'Dados do Entregador {entregador_id} atualizados com sucesso.'
        self.view.mostrar_mensagem(mensagem)

class UsuarioController:
    """ Classe responsável pelo controle do usuario """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def realizar_login(self, cpf, senha):
        """ Método responsável pelo controle do login de usuário """
        nome_usuario = self.model.fazer_login(cpf, senha)
        if nome_usuario:
            self.view.mostrar_mensagem(f"Bem-vindo, {nome_usuario}!")

    def realizar_logout(self):
        """ Método responsável pelo controle do logout de usuário """
        sucesso = self.model.fazer_logout()
        if sucesso:
            self.view.mostrar_mensagem("Logout bem-sucedido!")
        else:
            self.view.mostrar_mensagem("Falha ao fazer logout.")
