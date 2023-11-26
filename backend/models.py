# models.py
import psycopg2
import pika

# Model - Veiculo
class VeiculoModel:
    def __init__(self, database_config):
        self.database_config = database_config

    def cadastrar_veiculo(self, tipo, marca, modelo, ano, placa):
        try:
            with psycopg2.connect(**self.database_config) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO veiculos (tipo, marca, modelo, ano, placa) VALUES (%s, %s, %s, %s, %s)",
                               (tipo, marca, modelo, ano, placa))
                conn.commit()
                return True
        except psycopg2.Error as e:
            print(f"Ocorreu um erro ao acessar o banco de dados: {e}")
            return False

# Model - Cartao
class CartaoModel:
    def __init__(self, database_config, rabbitmq_config):
        self.database_config = database_config
        self.rabbitmq_config = rabbitmq_config

    def conectar_banco(self):
        return psycopg2.connect(**self.database_config)

    def cadastrar_cartao(self, cliente_id, tipo, numero):
        conn = self.conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO cartoes (cliente_id, tipo, numero) VALUES (%s, %s, %s)", (cliente_id, tipo, numero))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao cadastrar cartão: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def enviar_resposta_para_cliente(self, cliente_id, mensagem):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(**self.rabbitmq_config))
            channel = connection.channel()

            channel.queue_declare(queue=f'fila_respostas_{cliente_id}')
            channel.basic_publish(exchange='', routing_key=f'fila_respostas_{cliente_id}', body=mensagem)

            print(f'Mensagem enviada para o cliente {cliente_id}: {mensagem}')

            connection.close()

        except Exception as e:
            print(f"Ocorreu um erro ao conectar-se ao RabbitMQ: {e}")

# Model - Cliente
class ClienteModel:
    def __init__(self, database_config):
        self.database_config = database_config

    def conectar_banco(self):
        return psycopg2.connect(**self.database_config)

    def atualizar_cliente(self, cliente_id, novo_nome, novo_telefone):
        conn = self.conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE clientes SET nome = %s, telefone = %s WHERE id = %s",
                           (novo_nome, novo_telefone, cliente_id))
            conn.commit()
            print(f'Dados do Cliente {cliente_id} atualizados com sucesso.')
        except Exception as e:
            print(f"Erro ao atualizar dados do cliente: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

# Model - Entregador
class EntregadorModel:
    def __init__(self, database_config):
        self.database_config = database_config

    def conectar_banco(self):
        return psycopg2.connect(**self.database_config)

    def atualizar_entregador(self, entregador_id, novo_nome, novo_telefone):
        conn = self.conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE entregadores SET nome = %s, telefone = %s WHERE id = %s",
                           (novo_nome, novo_telefone, entregador_id))
            conn.commit()
            print(f'Dados do Entregador {entregador_id} atualizados com sucesso.')
        except Exception as e:
            print(f"Erro ao atualizar dados do entregador: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

# Model - Usuario
class UsuarioModel:
    def __init__(self, database_config):
        self.database_config = database_config

    def fazer_login(self, cpf, senha):
        try:
            with psycopg2.connect(**self.database_config) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM clientes WHERE cpf=%s AND senha=%s", (cpf, senha))
                usuario = cursor.fetchone()
                return usuario[1] if usuario else None  # Retorna o nome do usuário

        except psycopg2.Error as e:
            print(f"Ocorreu um erro ao acessar o banco de dados: {e}")
            return None

    def fazer_logout(self):
        return True  # Adapte conforme necessário
