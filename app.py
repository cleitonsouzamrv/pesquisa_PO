import streamlit as st
import pandas as pd
from PIL import Image
import base64
import json
import requests
import io
from datetime import datetime
from guia_lateral import mostrar_guia_lateral

# Configuração da página
st.set_page_config(
    page_title="Levantamento de Ferramentas e Painéis PBI",
    page_icon="logo_mrv_light.png",
    layout="wide"
)

with st.sidebar:
    logo = Image.open("logo_mrv_light.png")
    st.image(logo, width=240)
    st.title("Planejamento Operacional")
    st.markdown("### 📝 Levantamento de Ferramentas e Painéis")
    mostrar_guia_lateral()

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
    return response.status_code in [200, 201]

# ========= FORMULÁRIO =========
st.title("Pesquisa: Ferramentas e Painéis utilizados pela Equipe de Planejamento Operacional")
st.markdown(
    "Preencha as informações abaixo sobre os painéis e ferramentas que você utiliza no seu dia a dia.  \n"
    "Legenda: * Campos de preenchimento obrigatório."
)

st.subheader("👤 Identificação do usuário:")
email = st.text_input("Digite seu e-mail MRV (@mrv.com.br)*:")

# === PAINÉIS USADOS E FEEDBACKS ===
st.subheader("📊 Quais painéis abaixo você utiliza?")
paineis_lista = [
    "Painel Análises Forecast de Produção - PLNESROBR009",
    "Painel do Portifólio - Planejamento da Produção - PLNESROBR004",
    "Painel Operações - Planejamento e Controle - PLNESROBR010",
    "Painel Produção Produtividade e MO - PLNESROBR005",
    "PAP - Dossiê"
]
paineis_usados = st.multiselect("Selecione todos os painéis que você utiliza:* (Selecionar)", paineis_lista)

st.subheader("Deseja comentar sobre algum desses painéis?")
if "feedback_count" not in st.session_state:
    st.session_state.feedback_count = 1

feedbacks = {}
for i in range(st.session_state.feedback_count):
    cols = st.columns([2, 5])
    with cols[0]:
        painel = st.selectbox(f"Painel {i+1}", options=[""] + paineis_usados, key=f"painel_select_{i}")
    with cols[1]:
        if painel:
            feedback = st.text_area("Comentário", key=f"feedback_text_{i}")
            if painel and feedback:
                feedbacks[painel] = feedback

if st.button("Adicionar outro feedback"):
    st.session_state.feedback_count += 1
    st.rerun()

# === FERRAMENTAS ===
st.subheader("🔧 Ferramentas que você utiliza")
if "ferramenta_count" not in st.session_state:
    st.session_state.ferramenta_count = 1

ferramentas = []
ferramentas_resumo = []

categoria_lista = [
    "AUXÍLIO REGIONAL", "AMP X PLS", "DISCREPÂNCIA", "PROJECT",
    "ESTOQUE", "MOP/EMP", "CUSTOS", "REPLAN", "TURNOVER",
    "SEQUENCIAMENTO MO", "PRODUTIVIDADE", "HORAS EXTRAS", "OUTROS"
]

for i in range(st.session_state.ferramenta_count):
    st.markdown(f"---\n### Ferramenta {i+1}")
    linha1 = st.columns([3, 3])
    with linha1[0]:
        nome = st.text_input("Nome da Ferramenta* (Digitar)", key=f"nome_{i}")
    with linha1[1]:
        objetivo = st.text_input("Objetivo* (Digitar)", key=f"objetivo_{i}")

    linha2 = st.columns([2, 2, 2, 2])
    with linha2[0]:
        tipo = st.selectbox("Tipo* (Selecionar)", [
            "Power BI", "Excel", "Report e-mail", "Power Point",
            "Python", "Outra"
        ], key=f"tipo_{i}")
    with linha2[2]:
        importancia = st.selectbox("Importância* (Selecionar)", [
            "💎 Muito Importante", "🪙 Importante", "🟢 Pouco Importante", "🟠 Não Importante"
        ], key=f"importancia_{i}")
    with linha2[3]:
        horas = st.number_input("Horas gastas mensais* (Selecionar)", min_value=0.0, step=1.0, key=f"horas_{i}")

    with linha2[1]:
        categoria = st.selectbox("Categoria* (Selecionar)", categoria_lista, key=f"categoria_{i}")

    if nome.strip():
        ferramentas.append(f"{nome},{objetivo},{tipo},{categoria},{importancia},{horas}")
        ferramentas_resumo.append({
            "Nome": nome,
            "Objetivo": objetivo,
            "Tipo": tipo,
            "Categoria": categoria,
            "Importância": importancia,
            "Horas": horas
        })

if st.button("Adicionar nova Ferramenta"):
    st.session_state.ferramenta_count += 1
    st.rerun()

## === ENVIO E SALVAMENTO ===
if st.button("Salvar e Enviar Resposta"):
    erros = []
    if not email:
        erros.append("- E-mail MRV")
    if not ferramentas:
        erros.append("- Pelo menos uma ferramenta deve ser preenchida")

    if erros:
        st.error("Por favor, corrija os seguintes campos:\n" + "\n".join(erros))
    else:
        nova_resposta = {
            "E-mail MRV": email,
            "Data/Hora do Envio": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Painéis": "; ".join([f"{k}: {v}" for k, v in feedbacks.items()]),
            "Ferramentas": "; ".join(ferramentas)
        }

        df_novo = pd.DataFrame([nova_resposta])
        with st.spinner("Salvando resposta..."):
            df_existente, sha = carregar_planilha_do_github()
            if sha is None:
                st.error("❌ Não foi possível carregar a planilha do GitHub.")
            else:
                df_total = pd.concat([df_existente, df_novo], ignore_index=True)
                sucesso = salvar_planilha_no_github(df_total, sha)
                if sucesso:
                    st.success("✅ Resposta salva com sucesso. Agradecemos por sua contribuição!")
                    st.markdown(
                        "<h3>ℹ️ Gentileza, na pasta abaixo, faça o upload das ferramentas que você citou:<br>"
                        "link da pasta: <a href='https://mrvengenhariasa.sharepoint.com/:f:/s/PlanejamentoEstratgicodeObra/EqCtBFyFlLhKuW3NbOqI4KEB8YLkiAUnAt7XtTX6ve3FJA?e=TI40We' target='_blank'>Clique aqui</a></h3>",
                        unsafe_allow_html=True
                    )


                    with st.expander("🔍 Ver resumo do que foi enviado"):
                        st.markdown(f"**Email:** {email}")
                        st.markdown("**Painéis selecionados:**")
                        st.markdown(", ".join(paineis_usados) if paineis_usados else "_Nenhum painel selecionado_")
                        st.markdown("**Painéis comentados:**")
                        for painel, comentario in feedbacks.items():
                            st.markdown(f"- {painel}: {comentario}")
                        st.markdown("**Ferramentas preenchidas:**")
                        for idx, f in enumerate(ferramentas_resumo, 1):
                            st.markdown(f"{idx}. {f['Nome']} - {f['Objetivo']} ({f['Tipo']}/{f['Categoria']}) • {f['Importância']} • {f['Horas']}h/mês")
                    st.markdown("**Obrigado!**")
                    st.session_state.feedback_count = 1
                    st.session_state.ferramenta_count = 1
                else:
                    st.error("❌ Erro ao salvar a resposta no GitHub.")
