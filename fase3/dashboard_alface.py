import pandas as pd
import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="FarmTech Solutions - Dashboard Alface",
    layout="wide",
)


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    caminho_csv = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "leituras_irrigacao_alface.csv"
    )
    return pd.read_csv(caminho_csv)


df = carregar_dados()

st.title("FarmTech Solutions — Dashboard de Irrigação da Alface")

st.markdown(
    """
    Esta dashboard apresenta uma visualização dos dados simulados do sistema
    de irrigação inteligente da cultura da alface.
    Os dados foram gerados a partir da lógica dos sensores da Fase 2 e
    utilizados na importação para o banco Oracle na Fase 3.
    """
)

st.divider()

# Filtro lateral
status_opcoes = ["Todos"] + sorted(df["bomba_status"].unique().tolist())
status_selecionado = st.sidebar.selectbox(
    "Filtrar por status da bomba",
    status_opcoes,
)

if status_selecionado != "Todos":
    df_filtrado = df[df["bomba_status"] == status_selecionado].copy()
else:
    df_filtrado = df.copy()

st.sidebar.markdown("### Resumo do filtro")
st.sidebar.write(f"Total de leituras exibidas: {len(df_filtrado)}")

# Métricas principais
total_leituras = len(df_filtrado)
bomba_ligada = int((df_filtrado["bomba_status"] == "LIGADA").sum())
bomba_desligada = int((df_filtrado["bomba_status"] == "DESLIGADA").sum())
ph_medio = df_filtrado["ph_estimado"].mean()
umidade_media = df_filtrado["umidade_pct"].mean()
temperatura_media = df_filtrado["temperatura_c"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total de leituras", total_leituras)
col2.metric("Bomba ligada", bomba_ligada)
col3.metric("Bomba desligada", bomba_desligada)
col4.metric("pH médio", f"{ph_medio:.2f}")
col5.metric("Umidade média", f"{umidade_media:.1f}%")

st.metric("Temperatura média", f"{temperatura_media:.1f} °C")

st.divider()

# Gráfico de status da bomba
st.subheader("Status da bomba")

status_bomba = df_filtrado["bomba_status"].value_counts().reset_index()
status_bomba.columns = ["Status", "Total"]

st.bar_chart(
    data=status_bomba,
    x="Status",
    y="Total",
)

# Gráficos dos sensores
st.subheader("Evolução do pH estimado")
st.line_chart(
    data=df_filtrado,
    x="id_leitura",
    y="ph_estimado",
)

st.subheader("Evolução da umidade")
st.line_chart(
    data=df_filtrado,
    x="id_leitura",
    y="umidade_pct",
)

st.subheader("Evolução da temperatura")
st.line_chart(
    data=df_filtrado,
    x="id_leitura",
    y="temperatura_c",
)

# Recomendações
st.subheader("Resumo das recomendações")

recomendacoes = df_filtrado["recomendacao"].value_counts().reset_index()
recomendacoes.columns = ["Recomendação", "Total"]

st.dataframe(recomendacoes, use_container_width=True)

# Tabela completa
st.subheader("Base de dados completa")
st.dataframe(df_filtrado, use_container_width=True)
