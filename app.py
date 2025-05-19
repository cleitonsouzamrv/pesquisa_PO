import streamlit as st
import pandas as pd
from PIL import Image
import os

# Configuração da página
st.set_page_config(
    page_title="Levantamento de Ferramentas e Painéis PBI",
    page_icon="logo_mrv_light.png",
    layout="wide"
)

# Sidebar com logo
with st.sidebar:
    logo = Image.open("logo_mrv_light.png")
    st.image(logo, width=240)
    st.title("Levantamento de Ferramentas e Painéis PBI: Planejamento Operacional")
    st.markdown("Este aplicativo coleta informações sobre ferramentas e painéis utilizados pela equipe de Planejamento Operacional.")

# Conteúdo principal
st.title("Pesquisa: Ferramentas utilizadas pela Equipe de Planejamento Operacional")
st.markdown("Preencha as informações abaixo sobre as ferramentas e painéis de Power BI que você utiliza no seu dia a dia.")

# Campo de e-mail obrigatório
email = st.text_input("Seu e-mail MRV")

st.subheader("Ferramenta ou Painel 1")
ferramenta_1 = st.text_input("Nome da ferramenta ou painel")
categoria_1 = st.selectbox("Categoria", [
    "Painel Power BI", "Ferramenta de Planejamento", "Análise de Dados", "Automação", 
    "Controle Financeiro", "Gestão de Projetos", "Comunicação", "Outra"
])
impacto_1 = st.slider("Impacto no seu trabalho", 1, 5, 3)
comentario_1 = st.text_area("Comentários adicionais")

if st.button("Salvar e Enviar Resposta"):
    erros = []
    if not email:
        erros.append("- E-mail MRV")
    if not ferramenta_1:
        erros.append("- Nome da ferramenta ou painel")

    if erros:
        st.error("Por favor, preencha os seguintes campos obrigatórios:\n" + "\n".join(erros))
    else:
        nova_resposta = {
            "E-mail MRV": email,
            "Ferramenta/Painel": ferramenta_1,
            "Categoria": categoria_1,
            "Impacto": impacto_1,
            "Comentários": comentario_1
        }

        df_novo = pd.DataFrame([nova_resposta])
        caminho_arquivo = "respostas_levantamento_ferramentas.xlsx"

        if os.path.exists(caminho_arquivo):
            df_existente = pd.read_excel(caminho_arquivo)
            df_total = pd.concat([df_existente, df_novo], ignore_index=True)
        else:
            df_total = df_novo

        df_total.to_excel(caminho_arquivo, index=False)
        st.success("Resposta salva com sucesso!")
