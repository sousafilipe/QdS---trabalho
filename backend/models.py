""" O módulo psycopg2 é responsável por conectar o código com o banco de dados
    O módulo pika é responsável por fazer a conexão do servidor com o rabbitMQ """
import psycopg2
import pika


class VeiculoModel:
    """ Classe referente ao modelo veículo """
    def __init__(self, database_config):
        self.database_config = database_config

    def cadastrar_veiculo(self, tipo, marca, modelo, ano, placa):
        """ Método responsável por inserir o veículo no banco de dados """
        try:
            with psycopg2.connect(**self.database_config) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO veiculos (tipo, marca, modelo, ano, placa) "
                    "VALUES (%s, %s, %s, %s, %s)",
                               (tipo, marca, modelo, ano, placa))
                conn.commit()
                return True
        except psycopg2.Error as e:
            print(f"Ocorreu um erro ao acessar o banco de dados: {e}")
            return False


class CartaoModel:
    """ Classe referente ao modelo cartão """
    def __init__(self, database_config, rabbitmq_config):
        self.database_config = database_config
        self.rabbitmq_config = rabbitmq_config

    def conectar_banco(self):
        """ Método responsável por fazer a conexão do servidor com banco de dados """
        return psycopg2.connect(**self.database_config)

    def cadastrar_cartao(self, cliente_id, tipo, numero):
        """ Método responsável por inserir o cartão no banco de dados """
        conn = self.conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO cartoes (cliente_id, tipo, numero) VALUES (%s, %s, %s)",
            (cliente_id, tipo, numero))
            conn.commit()
            return True
        except psycopg2.IntegrityError as integrity_error:
            # Lidar com violação de integridade (por exemplo, chave única)
            print(f"Erro de integridade ao cadastrar cartão: {integrity_error}")
            return False

        except psycopg2.DataError as data_error:
            # Lidar com erros de dados (por exemplo, tipo de dados incorreto)
            print(f"Erro de dados ao cadastrar cartão: {data_error}")
            return False

        except psycopg2.DatabaseError as db_error:
            # Lidar com outros erros relacionados ao banco de dados
            print(f"Erro de banco de dados ao cadastrar cartão: {db_error}")
            return False
        finally:
            cursor.close()
            conn.close()

    def enviar_resposta_para_cliente(self, cliente_id, mensagem):
        """ Método responsável por dar o retorno da requisição do cliente """
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(**self.rabbitmq_config))
            channel = connection.channel()

            channel.queue_declare(queue=f'fila_respostas_{cliente_id}')
            channel.basic_publish(exchange='', routing_key=f'fila_respostas_{cliente_id}',
            body=mensagem)

            print(f'Mensagem enviada para o cliente {cliente_id}: {mensagem}')

            connection.close()

        except pika.exceptions.AMQPError as amqp_error:
            # Lidar com erros específicos do RabbitMQ
            print(f"Erro no RabbitMQ ao enviar mensagem para o cliente {cliente_id}: {amqp_error}")


class ClienteModel:
    """ Classe referente ao modelo Cliente """
    def __init__(self, database_config):
        self.database_config = database_config

    def conectar_banco(self):
        """ Método responsável por conectar com o banco de dados """
        return psycopg2.connect(**self.database_config)

    def atualizar_cliente(self, cliente_id, novo_nome, novo_telefone):
        """ Método responsável por atualizar os dados do cliente """
        conn = self.conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE clientes SET nome = %s, telefone = %s WHERE id = %s",
                           (novo_nome, novo_telefone, cliente_id))
            conn.commit()
            print(f'Dados do Cliente {cliente_id} atualizados com sucesso.')
        except psycopg2.IntegrityError as integrity_error:
            # Lidar com violação de integridade (por exemplo, chave única)
            print(f"Erro de integridade ao atualizar dados do cliente: {integrity_error}")
            conn.rollback()
        except psycopg2.DataError as data_error:
            # Lidar com erros de dados (por exemplo, tipo de dados incorreto)
            print(f"Erro de dados ao atualizar dados do cliente: {data_error}")
            conn.rollback()
        except psycopg2.DatabaseError as db_error:
            # Lidar com outros erros relacionados ao banco de dados
            print(f"Erro de banco de dados ao atualizar dados do cliente: {db_error}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

class EntregadorModel:
    """ Classe responsável pelo modelo do entregador """
    def __init__(self, database_config):
        self.database_config = database_config

    def conectar_banco(self):
        """ Responsável por conectar com o banco de dados """
        return psycopg2.connect(**self.database_config)

    def atualizar_entregador(self, entregador_id, novo_nome, novo_telefone):
        """ Método responsável por atualizar os dados do entregador """
        conn = self.conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE entregadores SET nome = %s, telefone = %s WHERE id = %s",
                           (novo_nome, novo_telefone, entregador_id))
            conn.commit()
            print(f'Dados do Entregador {entregador_id} atualizados com sucesso.')
        except psycopg2.IntegrityError as integrity_error:
            # Lidar com violação de integridade (por exemplo, chave única)
            print(f"Erro de integridade ao atualizar dados do entregador: {integrity_error}")
            conn.rollback()
        except psycopg2.DataError as data_error:
            # Lidar com erros de dados (por exemplo, tipo de dados incorreto)
            print(f"Erro de dados ao atualizar dados do entregador: {data_error}")
            conn.rollback()
        except psycopg2.DatabaseError as db_error:
            # Lidar com outros erros relacionados ao banco de dados
            print(f"Erro de banco de dados ao atualizar dados do entregador: {db_error}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


class UsuarioModel:
    """ Classe referente ao modelo usuario """
    def __init__(self, database_config):
        self.database_config = database_config

    def fazer_login(self, cpf, senha):
        """ Metodo responsavel por fazer login """
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
        """ Metodo para fazer logout """
        return True
