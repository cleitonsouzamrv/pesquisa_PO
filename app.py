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

# ========= FORMULÁRIO =========
st.title("Pesquisa: Ferramentas e Painéis utilizados pela Equipe de Planejamento Operacional")
st.markdown("Preencha as informações abaixo sobre os painéis e ferramentas que você utiliza no seu dia a dia.")

email = st.text_input("Seu e-mail MRV")

# === PAINÉIS USADOS E FEEDBACKS ===
st.subheader("Quais paineis abaixo você utiliza?")
paineis_lista = [
    "Painel Análises Forecast de Produção - PLNESROBR009",
    "Painel do Portifólio - Planejamento da Produção - PLNESROBR004",
    "Painel Operações - Planejamento e Controle - PLNESROBR010",
    "Painel Produção Produtividade e MO - PLNESROBR005",
    "PAP - Dossiê"
]
paineis_usados = st.multiselect("Selecione todos os paineis que você utiliza:", paineis_lista)

st.subheader("Deseja comentar sobre algum desses paineis?")
if "feedback_count" not in st.session_state:
    st.session_state.feedback_count = 1

feedbacks = {}
for i in range(st.session_state.feedback_count):
    cols = st.columns([2, 5])
    with cols[0]:
        painel = st.selectbox(
            f"Painel {i+1}",
            options=[""] + paineis_usados,
            key=f"painel_select_{i}"
        )
    with cols[1]:
        if painel:
            feedback = st.text_area(f"Comentário sobre o painel", key=f"feedback_text_{i}")
            if painel and feedback:
                feedbacks[painel] = feedback

if st.button("Adicionar outro feedback"):
    st.session_state.feedback_count += 1
    st.rerun()

# === FERRAMENTAS ===
st.subheader("Ferramentas que você utiliza")

if "ferramenta_count" not in st.session_state:
    st.session_state.ferramenta_count = 1

ferramentas = []

for i in range(st.session_state.ferramenta_count):
    st.markdown(f"**Ferramenta {i+1}**")
    cols = st.columns([2, 2, 2, 2, 2])
    with cols[0]:
        nome = st.text_input("Nome da Ferramenta", key=f"nome_{i}")
    with cols[1]:
        objetivo = st.text_input("Objetivo", key=f"objetivo_{i}")
    with cols[2]:
        categoria = st.selectbox("Categoria", [
            "Painel Power BI", "Ferramenta de Planejamento", "Análise de Dados", "Automação",
            "Controle Financeiro", "Gestão de Projetos", "Comunicação", "Outra"
        ], key=f"categoria_{i}")
    with cols[3]:
        importancia = st.selectbox("Importância (1-5)", [1, 2, 3, 4, 5], key=f"importancia_{i}")
    with cols[4]:
        horas = st.text_input("Horas gastas mensais", key=f"horas_{i}")

    ferramentas.append({
        "Nome da Ferramenta": nome,
        "Objetivo": objetivo,
        "Categoria da Ferramenta": categoria,
        "Importância": importancia,
        "Horas Gastas Mensais": horas
    })

if st.button("Adicionar nova Ferramenta"):
    st.session_state.ferramenta_count += 1
    st.rerun()

# === ENVIO ===
if st.button("Salvar e Enviar Resposta"):
    erros = []
    if not email:
        erros.append("- E-mail MRV")

    ferramentas_validas = [f for f in ferramentas if f["Nome da Ferramenta"].strip()]
    if not ferramentas_validas:
        erros.append("- Pelo menos uma ferramenta deve ser preenchida")

    if erros:
        st.error("Por favor, preencha os seguintes campos obrigatórios:\n" + "\n".join(erros))
    else:
        nova_resposta = {
            "E-mail MRV": email,
            "Paineis Utilizados": "; ".join(paineis_usados),
            "Feedbacks dos Paineis": "; ".join([f"{k}: {v}" for k, v in feedbacks.items()]),
            "Data/Hora do Envio": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        for j, ferramenta in enumerate(ferramentas_validas, start=1):
            for k, v in ferramenta.items():
                nova_resposta[f"{k} {j}"] = v

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
                    st.session_state.feedback_count = 1
                    st.session_state.ferramenta_count = 1
                else:
                    st.error("❌ Erro ao salvar a resposta no GitHub. Verifique o token e permissões.")
