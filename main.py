""" Pika e o modulo reponsavel pela interacao com o rabbitmq """
import pika
from backend.models import VeiculoModel, CartaoModel, ClienteModel, EntregadorModel, UsuarioModel
from backend.views import ClienteView, CartaoView, EntregadorView, UsuarioView
from backend.controllers import VeiculoController, CartaoController, \
    ClienteController,EntregadorController, UsuarioController

# Configurações do banco de dados
database_config = {
    'database': 'itadelivery',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

# Configurações do RabbitMQ
rabbitmq_config = {
    'host': 'localhost',
    'port': 5672,
    'credentials': pika.PlainCredentials('admin', '1234')
}

# Criar instâncias dos modelos
veiculo_model = VeiculoModel(database_config)
cartao_model = CartaoModel(database_config, rabbitmq_config)
cliente_model = ClienteModel(database_config)
entregador_model = EntregadorModel(database_config)
usuario_model = UsuarioModel(database_config)

# Criar instâncias das visões
cliente_view = ClienteView()
cartao_view = CartaoView()
entregador_view = EntregadorView()
usuario_view = UsuarioView()

# Criar instâncias dos controladores
veiculo_controller = VeiculoController(veiculo_model)
cartao_controller = CartaoController(cartao_model, cartao_view)
cliente_controller = ClienteController(cliente_model, cliente_view)
entregador_controller = EntregadorController(entregador_model, entregador_view)
usuario_controller = UsuarioController(usuario_model, usuario_view)

# Testar algumas funcionalidades
veiculo_controller.cadastrar_veiculo('Carro', 'Ford', 'Fiesta', 2022, 'ABC1234')

cliente_controller.atualizar_cliente(1, 'mauricio', '8599999999')

entregador_controller.atualizar_entregador(1, 'poo Nelson', '999999999')

usuario_controller.realizar_login('123456789', 'senha123')

cartao_controller.cadastrar_cartao(1, 'Débito', '987654321')

usuario_controller.realizar_logout()
