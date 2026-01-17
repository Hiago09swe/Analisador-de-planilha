import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dash Automático", layout="wide")

st.title("📊 Dashboard Gerador Automático")
st.subheader("Suba sua planilha e visualize os dados instantaneamente")

# Upload do arquivo
uploaded_file = st.file_uploader("Escolha um arquivo CSV ou Excel", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Carregamento dos dados
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("Dados carregados com sucesso!")
        
        # --- SIDEBAR: Filtros Dinâmicos ---
        st.sidebar.header("Configurações do Dashboard")
        
        # Identificar tipos de colunas
        cols_numericas = df.select_dtypes(include=['float', 'int']).columns.tolist()
        cols_objetos = df.select_dtypes(include=['object', 'category']).columns.tolist()

        # Seleção de colunas para os eixos
        eixo_x = st.sidebar.selectbox("Escolha o eixo X (Categorias)", cols_objetos if cols_objetos else df.columns)
        eixo_y = st.sidebar.selectbox("Escolha o eixo Y (Valores)", cols_numericas if cols_numericas else df.columns)
        
        # --- DASHBOARD PRINCIPAL ---
        
        # KPI's Simples
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Linhas", df.shape[0])
        with col2:
            if cols_numericas:
                st.metric(f"Soma de {eixo_y}", f"{df[eixo_y].sum():,.2f}")
        with col3:
            st.metric("Total de Colunas", df.shape[1])

        st.divider()

        # Gráficos
        c1, c2 = st.columns(2)

        with c1:
            st.write(f"### Distribuição de {eixo_y} por {eixo_x}")
            fig_bar = px.bar(df, x=eixo_x, y=eixo_y, color=eixo_x, template="plotly_white")
            st.plotly_chart(fig_bar, use_container_width=True)

        with c2:
            st.write(f"### Participação (Pizza)")
            fig_pie = px.pie(df, names=eixo_x, values=eixo_y, hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)

        # Visualização da Tabela
        with st.expander("Ver dados brutos"):
            st.write(df)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")

else:
    st.info("Aguardando arquivo... Por favor, suba uma planilha para começar.")