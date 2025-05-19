import streamlit as st
import pandas as pd
from PIL import Image
import base64
import json
import requests
import io
from datetime import datetime

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

# GitHub config
GITHUB_TOKEN = st.secrets["github"]["token"]
GITHUB_USERNAME = st.secrets["github"]["username"]
REPO_NAME = st.secrets["github"]["repo"]
FILE_PATH = st.secrets["github"]["file_path"]
BRANCH = st.secrets["github"]["branch"]

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def carregar_planilha_do_github():
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        content = base64.b64decode(r.json()["content"])
        return pd.read_excel(io.BytesIO(content)), r.json()["sha"]
    else:
        return pd.DataFrame(), None

def salvar_planilha_no_github(df, sha):
    output = io.BytesIO()
    df.to_excel(output, index=False)
    content_encoded = base64.b64encode(output.getvalue()).decode("utf-8")
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"
    data = {
        "message": "Atualizando base de dados da pesquisa via Streamlit",
        "content": content_encoded,
        "branch": BRANCH,
        "sha": sha
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    return response.status_code == 201 or response.status_code == 200

# Formulário
st.title("Pesquisa: Ferramentas utilizadas pela Equipe de Planejamento Operacional")
st.markdown("Preencha as informações abaixo sobre as ferramentas e painéis de Power BI que você utiliza no seu dia a dia.")

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
            "Comentários": comentario_1,
            "Data/Hora do Envio": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df_novo = pd.DataFrame([nova_resposta])

        with st.spinner("Salvando resposta..."):
            df_existente, sha = carregar_planilha_do_github()

            if sha is None:
                st.error("❌ Não foi possível carregar a planilha do GitHub. A resposta não foi salva.")
            else:
                df_total = pd.concat([df_existente, df_novo], ignore_index=True)
                sucesso = salvar_planilha_no_github(df_total, sha)

                if sucesso:
                    st.success("✅ Resposta salva com sucesso no GitHub!")
                else:
                    st.error("❌ Erro ao salvar a resposta no GitHub. Verifique o token e permissões.")
