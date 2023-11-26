# Sistema de Entregas - Itadelivery

## Descrição

Este projeto foi criado para a disciplina de Qualidade de software, e esse projeto é a refatoração e reengenharia do código do projeto integrador "Itadelivery", um aplicativo fictício de entregas. O projeto inicialmente continha código procedural e organizado em pastas, que foi transformado em um modelo orientado a objetos (POO) usando a arquitetura Modelo-Visão-Controlador (MVC).

![Portal da UFC - Universidade Federal do Ceará - Assinatura Horizontal do  Brasão da UFC](https://www.ufc.br/images/_images/a_universidade/identidade_visual/brasao/brasao1_horizontal_cor_72dpi.png)

## Estrutura do Projeto

- **models.py**: Contém as classes de modelos que representam as entidades do sistema, como veículos, cartões, clientes, entregadores e usuários.

- **views.py**: Define classes de visualização para exibir mensagens no console.

- **controllers.py**: Implementa controladores para orquestrar as operações do sistema, conectando modelos e visões.

- **main.py**: Script principal onde instâncias dos modelos, visões e controladores são criadas. Ele inclui testes simulados para demonstrar o funcionamento do sistema.

## Como Executar

Certifique-se de ter Python instalado em seu sistema. Você também pode precisar instalar as dependências usando o seguinte comando:

```bash
pip install psycopg2 pika
```

Para executar o sistema, basta rodar o script `main.py`:

```
python main.py
```

## Configurações

As configurações do banco de dados PostgreSQL e do RabbitMQ podem ser ajustadas no arquivo `main.py`.

## Notas Adicionais

Este projeto é um exercício de refatoração do código para o projeto integrador "Itadelivery", um aplicativo de entregas. O código original era procedural e foi transformado em POO, seguindo a arquitetura MVC. Este repositório contém apenas o código referente ao backend e um teste na main.

Em um ambiente de produção, você precisaria expandir e adaptar o código de acordo com os requisitos específicos do seu projeto.

