import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime
import time
import streamlit_authenticator as stauth

conn = sqlite3.connect("academia.db", check_same_thread=False)
cursor = conn.cursor()



cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade TEXT NOT NULL,
    sexo TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL,
    plano_id INTEGER NOT NULL,
    instrutor_id INTEGER NOT NULL,
    treino_id INTEGER NOT NULL,
    FOREIGN KEY(instrutor_id) REFERENCES instrutores(id),
    FOREIGN KEY(treino_id) REFERENCES treino(id),       
    FOREIGN KEY(plano_id) REFERENCES planos(id)      
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS instrutores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    especialidade TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS planos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco_mensal TEXT NOT NULL,
    duracao_meses INTEGER NOT NULL
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS treino_exercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    treino_id INTEGER NOT NULL,
    treino TEXT NOT NULL,
    exercicio_id INTEGER NOT NULL,
    exercicio TEXT NOT NULL,
    series TEXT NOT NULL,
    repeticoes INTEGER NOT NULL,
    FOREIGN KEY(treino_id) REFERENCES treinos(id),
    FOREIGN KEY(exercicio_id) REFERENCES exercicios(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pagamento_clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    plano_id INTEGER NOT NULL,
    data_pagamento TEXT NOT NULL,
    valor_pago REAL NOT NULL,
    FOREIGN KEY(cliente_id) REFERENCES clientes(id),
    FOREIGN KEY(plano_id) REFERENCES planos(id)
)
''')

conn.commit()

conn = sqlite3.connect('academia.db')
cursor = conn.cursor()


def importar_csv(arquivo, tabela, colunas):
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
    count = cursor.fetchone()[0]
    if count == 0:  
        df = pd.read_csv(arquivo)
        df.to_sql(tabela, conn, if_exists='append', index=False)
        print(f"Dados importados para a tabela '{tabela}'.")
    else:
        print(f"Tabela '{tabela}' já contém dados. Importação ignorada.")



importar_csv('clientes_academia.csv', 'clientes', ['id', 'nome','idade','sexo', 'email', 'telefone', 'plano_id', 'instrutor_id', 'treino_id'])
importar_csv('instrutores.csv', 'instrutores', ['id', 'nome', 'especialidade'])
importar_csv('planos.csv', 'planos', ['id', 'nome', 'preco_mensal', 'duracao_meses'])
importar_csv('treino_exercicios.csv', 'treino_exercicios', ['id', 'treino_id','treino','exercicio_id','exercicio','series', 'repeticoes'])
importar_csv('pagamento_clientes.csv', 'pagamento_clientes', ['id', 'cliente_id','plano_id','data_pagamento','valor_pago'])

conn.commit()

st.sidebar.title("📋Menu")
menu = st.sidebar.selectbox("Categorias: ", ["🏠 Home","🔐 Login","👤 Cliente", "💰 Pagamento", "🏋️ Treino","🧗‍♀️ Portal do Cliente"])

if(menu == "🏠 Home"):
    st.header("🏠 Página Inicial", divider = True)
    st.subheader("Projeto em grupo Sistema para uma Academia.")
    st.write("""**Integrantes:**""")

    st.write("""
            - Matheus Henrique Martineli Fernandes\n		
            - Flavio Gabriel Barto Machado\n		
            - Pedro Lucas Marlier Alves\n		
            - Flavia Luisa Barbosa\n		
            - Luiz Alexandre Nishiyama Galvani\n
    """)

    st.subheader("""**Descrição do Projeto:**""")
    st.write("""
                Este projeto foi desenvolvido em grupo com o objetivo principal de promover a participação colaborativa entre os integrantes e fortalecer nossas habilidades
                técnicas e práticas. Durante o desenvolvimento, aplicamos conhecimentos de banco de dados, programação e criação de interfaces para construir um sistema de gestão para academias.

                Além de criar uma ferramenta funcional para cadastro e gerenciamento de clientes, planos, treinos e pagamentos, o projeto serve como um espaço para aprendermos a trabalhar em equipe,
                dividir tarefas, resolver problemas e melhorar nossa capacidade de comunicação e desenvolvimento conjunto.
    """)

if(menu == "🔐 Login"):
    st.header("🔐 Login", divider = True)
    # usernames = ['ADM', 'ClienteX']
    # names = ['Luiz', 'Dani']
    # passwords = ['1234567890', '0987654321']
    # statusLogin = False
    
   
    # if statusLogin:
    #     st.success(f"Bem-vindo, {name}!")

        
    # elif statusLogin == False:
    #     st.error("Usuário ou senha inválidos")
    # else:
    #     st.warning("Insira suas credenciais")

if(menu == "🧗‍♀️ Portal do Cliente"):
    st.header("🧗‍♀️ Portal do Cliente", divider = True)

    st.subheader("🔍 Filtragem de treinos e exercícios", divider=True)
    treinos = pd.read_sql_query("""
                    SELECT DISTINCT treino
                    FROM treino_exercicios
                    """, conn)
    filtro_treino = st.selectbox("Escolha o treino", treinos['treino'].unique())
    exercicio_filtrados = pd.read_sql_query(
        "SELECT exercicio FROM treino_exercicios WHERE treino = ?", conn, params=(filtro_treino,))
    st.dataframe(exercicio_filtrados)

    st.subheader("👨‍🏫 Instrutores:", divider=True)
    instrutores = pd.read_sql_query('''
        SELECT i.nome AS nome_do_instrutor
        FROM instrutores i
    ''', conn)
    st.dataframe(instrutores)

    st.subheader("📚 Info. Planos:", divider=True)
    planos = ['Basic', 'Premium', 'VIP']
    tipoPlano = st.selectbox('Plano:' ,planos)
    if(tipoPlano == 'Basic'):
        st.write("""
                    **Plano Basic**\n
                    Plano básico para quem quer começar a se exercitar. Acesso à academia durante horários limitados, uso livre dos equipamentos e participação em aulas básicas em grupo.
                """)
    elif(tipoPlano == 'Premium'):
        st.write("""
                    **Plano Premium**\n
                    Plano intermediário com acesso livre durante todo o horário de funcionamento. Inclui aulas avançadas, acompanhamento mensal com personal trainer e acesso à sauna.
                """)
    else:
        st.write("""
                    **Plano VIP**\n
                    Plano completo para quem busca o máximo de benefícios. Acesso 24 horas, aulas exclusivas, sessões regulares com personal trainer, avaliação física detalhada e acesso
                    a todas as áreas VIP, como piscina e spa.

                """)

    st.subheader("Horários de Funcionamento da Academia:", divider = True)
    st.write("""
            **Plano Basic:**\n
            Segunda a Sexta-feira: 06:00 - 12:00

            Sábado: 08:00 - 12:00

            Domingo: Fechado

            Observação: Usuários do plano Basic têm acesso apenas durante o horário da manhã nos dias úteis e apenas até o meio-dia no sábado.
            """)
    st.subheader("",divider = True)
    st.write("""
            **Plano Premium:**\n
            Segunda a Sexta-feira: 06:00 - 22:00

            Sábado: 08:00 - 18:00

            Domingo: 10:00 - 14:00

            Observação: Usuários do plano Premium têm acesso durante o dia todo, com um horário reduzido no domingo.
            """)
    st.subheader("",divider = True)
    st.write("""
            **Plano VIP:**\n
            Segunda a Domingo: 24 horas por dia (Acesso completo)

            Observação: Usuários do plano VIP podem acessar a academia a qualquer hora do dia, todos os dias da semana, com total flexibilidade.
            """)

    st.subheader("Sobre a Academia",divider = True)
    st.write("""
            **Endereço:**\n
            Rua ABC 950, Londrina-PR 
            """)

if(menu == "👤 Cliente"):
    st.header("👤 Cliente", divider = True)

    st.subheader("Lista de Clientes e seus Planos")

    df_lista = pd.read_sql_query('''
        SELECT c.nome, c.plano_id AS plano_id, p.nome AS plano
        FROM clientes c
        JOIN planos p ON c.plano_id = p.id
    ''', conn)

    st.dataframe(df_lista)

    planos = ['Basic', 'Premium', 'VIP']
    instrutores = ['Carlos Rocha', 'Fernanda Lima', 'João Mendes']
 
    if 'reset' not in st.session_state:
        st.session_state.reset = False
    if st.session_state.reset:
        st.session_state['nome'] = ""
        st.session_state['idade'] = 0
        st.session_state['sexo'] = "M"
        st.session_state['email'] = ""
        st.session_state['telefone'] = ""
        st.session_state['plano_selecionado'] = "Basic"
        st.session_state['instrutores_selecionado'] = "Carlos Rocha"
        st.session_state['treino_id'] = 1
        st.session_state.reset = False

    st.subheader("📝Cadastro de Clientes", divider = True)

    nome = st.text_input("Nome:", key = 'nome')

    idade = st.number_input("Idade:", min_value=0, max_value=120, key = 'idade')

    sexo = st.selectbox("Sexo:", ["M", "F"], key = 'sexo')

    email = st.text_input("Email:", key = 'email')

    telefone = st.text_input("Telefone:", key = 'telefone')

    plano_selecionado = st.selectbox("Plano:", planos, key = 'plano_selecionado')
    indice = planos.index(plano_selecionado)
    plano_id = indice + 1

    instrutores_selecionado = st.selectbox("Instrutores:", instrutores, key = 'instrutores_selecionado')
    indiceInstrutores = instrutores.index(instrutores_selecionado)
    instrutor_id = indiceInstrutores + 1


    treino_id = st.number_input("ID do Treino", min_value=1, key = 'treino_id')

    if st.button("Cadastrar Cliente"):
        cursor.execute("""
            INSERT INTO clientes (nome, idade, sexo, email, telefone, plano_id, instrutor_id, treino_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome, idade, sexo, email, telefone, plano_id, instrutor_id, treino_id))
        conn.commit()
        st.success("Cliente cadastrado com sucesso!")
        time.sleep(2)
        st.session_state.reset = True
        
        st.rerun()

if(menu == "💰 Pagamento"):
    st.header("💰 Pagamento", divider = True)  

    st.subheader("💸 Total de pagamentos e último pagamento por cliente", divider=True)
    total_pagamentos = pd.read_sql_query('''
        SELECT c.nome AS nome_do_cliente, SUM(pc.valor_pago) AS total_pago, MAX(pc.data_pagamento) AS ultimo_pagamento
        FROM pagamento_clientes pc
        JOIN clientes c ON pc.cliente_id = c.id
        GROUP BY c.id
    ''', conn)
    st.dataframe(total_pagamentos)

    st.subheader("➕ Inserir novo pagamento")
    with st.form("form_inserir"):
        cliente_id = st.text_input("Informe o ID do cliente")
        plano_id = st.text_input("Informe o ID do plano")
        valor_pago = st.text_input("Valor pago:")
        data_pagamentos = st.text_input("📅 Insira data pagamento:")
        enviar = st.form_submit_button("Inserir")

    if enviar and cliente_id.strip():
        erro = False

        try:
            data_pagamentos = datetime.strptime(data_pagamentos, "%d-%m-%Y").strftime("%d-%m-%Y")
        except ValueError:
            st.error("Formato de data inválido! Use o formato DD-MM-AAAA.")
            erro = True


        plano_id = int(plano_id) if plano_id.isdigit() else None
        valor_pago = float(valor_pago) if valor_pago.replace('.', '', 1).isdigit() else None

        if plano_id == 1 and valor_pago != 100:
            st.error("Erro no pagamento: O plano 1 requer um pagamento de 100.")
            erro = True
        elif plano_id == 2 and valor_pago != 200:
            st.error("Erro no pagamento: O plano 2 requer um pagamento de 200.")
            erro = True
        elif plano_id == 3 and valor_pago != 300:
            st.error("Erro no pagamento: O plano 3 requer um pagamento de 300.")
            erro = True

        if not erro:
            cursor.execute("INSERT INTO pagamento_clientes (cliente_id, plano_id, valor_pago, data_pagamento) VALUES (?,?,?,?)",
                        (cliente_id, plano_id, valor_pago, data_pagamentos))
            conn.commit()
            st.rerun()




if(menu == "🏋️ Treino"):
    st.header("🏋️ Treino", divider = True)

    st.subheader("🔍 Filtragem de treinos e exercícios", divider=True)
    treinos = pd.read_sql_query("SELECT DISTINCT treino FROM treino_exercicios", conn)
    filtro_treino = st.selectbox("Escolha o treino", treinos['treino'].unique())
    exercicio_filtrados = pd.read_sql_query(
        "SELECT exercicio FROM treino_exercicios WHERE treino = ?", conn, params=(filtro_treino,))
    st.dataframe(exercicio_filtrados)

    st.subheader("👨‍🏫 Quantos clientes cada instrutor atende", divider=True)
    instrutores_clientes = pd.read_sql_query('''
        SELECT i.nome AS nome_do_instrutor, COUNT(c.id) AS total_clientes
        FROM instrutores i
        JOIN clientes c on i.id = c.instrutor_id
        GROUP BY i.id
    ''', conn)
    st.dataframe(instrutores_clientes)
    st.subheader("➕ Inserir novo treino")
    with st.form("form_inserir2"):
        treino_id = st.text_input("Informe o ID do treino")
        treino = st.text_input("Informe o treino")
        exercicio_id = st.text_input("Informe o ID do exercicio:")
        exercicio = st.text_input("Informe o exercicio:")
        serie = st.text_input("Informe quantas séries:")
        repeticao = st.text_input("Informe quantas repetições:")
        enviar = st.form_submit_button("Inserir")

    if enviar and treino.strip():
        cursor.execute("INSERT INTO treino_exercicios (treino_id, treino, exercicio_id, exercicio,series,repeticoes) VALUES (?,?,?,?,?,?)",
                        (treino_id, treino, exercicio_id, exercicio,serie,repeticao))
        conn.commit()
        st.success("Treino Cadastrado com Sucesso!!!")
        st.rerun()  



conn.close()
