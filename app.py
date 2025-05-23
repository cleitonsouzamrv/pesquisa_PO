# Importação de bibliotecas necessárias
import streamlit as st  # Framework principal para criação da interface web
import pandas as pd  # Manipulação de dados
from PIL import Image  # Manipulação de imagens
import base64  # Codificação/decodificação base64 (para comunicação com GitHub)
import json  # Manipulação de objetos JSON
import requests  # Realização de requisições HTTP
import io  # Manipulação de fluxos de dados binários
from datetime import datetime  # Manipulação de datas e horários
from guia_lateral import mostrar_guia_lateral  # Função personalizada para mostrar guia lateral

# =========================== CONFIGURAÇÃO DA PÁGINA ===========================

# Definição das configurações da página web no Streamlit
st.set_page_config(
    page_title="Pesquisa: Ferramentas e Painéis",
    page_icon="logo_mrv_light.png",
    layout="wide"
)

# Configuração da barra lateral
with st.sidebar:
    logo = Image.open("logo_mrv_light.png")  # Carrega a imagem do logo
    st.image(logo, width=240)  # Exibe o logo na barra lateral
    st.title("Planejamento Operacional")
    st.markdown("## 📝 Levantamento de Ferramentas e Painéis")
    mostrar_guia_lateral()  # Exibe a guia lateral personalizada

# =========================== CONFIGURAÇÃO DO GITHUB ===========================

# Credenciais e informações do repositório GitHub via secrets
GITHUB_TOKEN = st.secrets["github"]["token"]
GITHUB_USERNAME = st.secrets["github"]["username"]
REPO_NAME = st.secrets["github"]["repo"]
FILE_PATH = st.secrets["github"]["file_path"]
BRANCH = st.secrets["github"]["branch"]

# Cabeçalho de autenticação para requisições à API do GitHub
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Função para carregar a planilha existente no repositório do GitHub
def carregar_planilha_do_github():
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        content = base64.b64decode(r.json()["content"])
        return pd.read_excel(io.BytesIO(content)), r.json()["sha"]
    else:
        return pd.DataFrame(), None

# Função para salvar a planilha atualizada de volta ao GitHub
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

# =========================== FORMULÁRIO PRINCIPAL ===========================

# Título e instruções
st.title("Pesquisa: Ferramentas e Painéis utilizados pela Equipe de Planejamento Operacional")
st.markdown(
    "Preencha as informações abaixo sobre os painéis e ferramentas que você utiliza no seu dia a dia.  \n"
    "Legenda: * Campos de preenchimento obrigatório."
)

# Campo de identificação do usuário
st.subheader("👤 Identificação do usuário:")
email = st.text_input("Digite seu e-mail MRV (@mrv.com.br)*:")

# =========================== PAINÉIS USADOS E FEEDBACKS ===========================

st.subheader("📊 Quais painéis abaixo você utiliza?")

paineis_lista = [
    "Painel Análises Forecast de Produção - PLNESROBR009",
    "Painel do Portifólio - Planejamento da Produção - PLNESROBR004",
    "Painel Operações - Planejamento e Controle - PLNESROBR010",
    "Painel Produção Produtividade e MO - PLNESROBR005",
    "PAP - Dossiê",
    "Painel AMP x PLS - CST002", 
    "Painel Acompanhamento de Concreto - ENGPDC032",
    "Painel Book Normas - ENGPDC018", 
    "Painel Cheque Obra - ENGPDC015",
    "Painel Cockpit Produção - ENGPDC010", 
    "Painel Comunicação Integrada - ENGPDC028",
    "Painel Custos Produção - ENGPDC009", 
    "Painel de Materiais - ENGPDC005",
    "Painel Gestão de Acesso Obras - ENGPDC011", 
    "Painel Obra 360 - ENGPDC035",
    "Painel Performance da Produção - ENGPDC029", 
    "Painel Qualidade - ENGPDC007",
    "Painel SSMA Regionais - ENGPDC030", 
    "Relatório de Métricas de Preços e Serviços - ENGPDC004",
    "Painel Gestão de Problema Pós Entrega - ASTTCN006",
    "Painel Vistoria da Qualidade - ASTTCN010"
]

# Multiselect para selecionar painéis utilizados
paineis_usados = st.multiselect("Selecione todos os painéis que você utiliza:* (Selecionar)", paineis_lista)

# Seção de feedback sobre painéis
st.subheader("Avalie os painéis selecionados e deixe seu feedback:")

feedbacks = {}  # Dicionário para armazenar os feedbacks e avaliações

# Para cada painel selecionado, gera uma linha com: nome, nota, comentário
for painel in paineis_usados:
    cols = st.columns([2, 1, 3])  # Dimensionar tamanho: Nome do painel | Nota | Comentário

    with cols[0]:
        st.markdown(
            f"<span style='font-size:14px;'>{painel}</span>", 
            unsafe_allow_html=True
        )

    with cols[1]:
        nota = st.number_input(
            label="Nota (0-10)*",
            min_value=0,
            max_value=10,
            step=1,
            key=f"nota_{painel}"
        )

    with cols[2]:
        comentario = st.text_input(
            label="Comentário (opcional)",
            placeholder="Escreva ou deixe em branco",
            key=f"comentario_{painel}"
        )

    # Armazena como dicionário: {comentario: ..., nota: ...}
    feedbacks[painel] = {"comentario": comentario, "nota": nota}


# =========================== FERRAMENTAS ===========================

st.subheader("🔧 Ferramentas que você utiliza")
if "ferramenta_count" not in st.session_state:
    st.session_state.ferramenta_count = 1  # Inicializa o contador de ferramentas

ferramentas = []  # Lista para armazenar as ferramentas como texto
ferramentas_resumo = []  # Lista para armazenar as ferramentas como dicionário

# Lista de categorias para seleção
categoria_lista = [
    "AUXÍLIO REGIONAL", "AMP X PLS", "DISCREPÂNCIA", "PROJECT",
    "ESTOQUE", "MOP/EMP", "CUSTOS", "REPLAN", "TURNOVER",
    "SEQUENCIAMENTO MO", "PRODUTIVIDADE", "HORAS EXTRAS", "OUTROS"
]

# Lista para armazenar índices que devem ser removidos
remover_indices = []

# Loop para criar campos dinâmicos de ferramentas
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
            "Python", "SAP BO + Excel", "BIG + Excel", "Outra"
        ], key=f"tipo_{i}")
    with linha2[2]:
        importancia = st.selectbox("Importância* (Selecionar)", [
            "💎 Muito Importante", "🪙 Importante", "🟢 Pouco Importante", "🟠 Não Importante"
        ], key=f"importancia_{i}")
    with linha2[3]:
        horas = st.number_input("Horas gastas mensais* (Selecionar)", min_value=0.0, step=1.0, key=f"horas_{i}")
    with linha2[1]:
        categoria = st.selectbox("Categoria* (Selecionar)", categoria_lista, key=f"categoria_{i}")

    # Botão de remoção para esta ferramenta
    if st.button(f"🗑️ Remover Ferramenta {i+1}"):
        remover_indices.append(i)


    # Armazena a ferramenta preenchida
    if nome.strip():
        ferramenta_dict = {
            "Nome": nome,
            "Objetivo": objetivo,
            "Tipo": tipo,
            "Categoria": categoria,
            "Importância": importancia,
            # ✅ Aqui garantimos que sempre será um float
            "Horas": float(horas) if isinstance(horas, (int, float)) else 0.0
        }
        ferramentas.append(json.dumps(ferramenta_dict, ensure_ascii=False))
        ferramentas_resumo.append(ferramenta_dict)



# Remove as ferramentas marcadas
if remover_indices:
    for idx in sorted(remover_indices, reverse=True):
        for key in ["nome_", "objetivo_", "tipo_", "categoria_", "importancia_", "horas_"]:
            st.session_state.pop(f"{key}{idx}", None)
    st.session_state.ferramenta_count -= len(remover_indices)
    st.rerun()

# Botão para adicionar nova ferramenta
if st.button("➕ Adicionar nova Ferramenta"):
    st.session_state.ferramenta_count += 1
    st.rerun()


# =========================== ENVIO E SALVAMENTO ===========================

if st.button("💾 Salvar e Enviar Resposta"):
    erros = []

    # Validação de campos obrigatórios por ferramenta
    for idx, f in enumerate(ferramentas_resumo, 1):
        if not f["Nome"] or not str(f["Nome"]).strip():
            erros.append(f"- Nome da Ferramenta {idx} não preenchido")
        if not f["Objetivo"] or not str(f["Objetivo"]).strip():
            erros.append(f"- Objetivo da Ferramenta {idx} não preenchido")
        if not f["Tipo"] or f["Tipo"] == "Selecione":
            erros.append(f"- Tipo da Ferramenta {idx} não selecionado")
        if not f["Categoria"] or f["Categoria"] == "Selecione":
            erros.append(f"- Categoria da Ferramenta {idx} não selecionada")
        if not f["Importância"] or f["Importância"] == "Selecione":
            erros.append(f"- Importância da Ferramenta {idx} não selecionada")
        if f["Horas"] is None or f["Horas"] == "" or f["Horas"] == 0:
            erros.append(f"- Horas gastas da Ferramenta {idx} não preenchidas ou igual a 0")

    # Exibe os erros e interrompe o fluxo
    if erros:
        st.error("Por favor, corrija os seguintes campos:\n" + "\n".join(erros))
    else:
        # Monta a nova resposta como dicionário
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
                            st.markdown(
                                f"{idx}. {f['Nome']} - {f['Objetivo']} ({f['Tipo']}/{f['Categoria']}) • {f['Importância']} • {f['Horas']}h/mês"
                            )

                    st.markdown("**Obrigado!**")

                    # Botão para reiniciar o formulário
                    if st.button("🔄 Fazer nova pesquisa"):
                        # Reset das variáveis
                        st.session_state.ferramenta_count = 1

                        for i in range(0, 100):
                            st.session_state.pop(f"nome_{i}", None)
                            st.session_state.pop(f"objetivo_{i}", None)
                            st.session_state.pop(f"tipo_{i}", None)
                            st.session_state.pop(f"categoria_{i}", None)
                            st.session_state.pop(f"importancia_{i}", None)
                            st.session_state.pop(f"horas_{i}", None)

                        for painel in paineis_lista:
                            st.session_state.pop(f"nota_{painel}", None)
                            st.session_state.pop(f"comentario_{painel}", None)

                        # Também limpar e-mail se quiser:
                        st.session_state.pop("email", None)

                        # Forçar recarregamento com tudo limpo
                        st.experimental_rerun()

                else:
                    st.error("❌ Erro ao salvar a resposta no GitHub.")


