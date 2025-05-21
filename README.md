# pesquisa_PO

📝 Levantamento de Ferramentas e Painéis PBI
    📋 Descrição do Projeto
Este projeto consiste em uma aplicação web interativa desenvolvida com Streamlit que permite a coleta estruturada de informações sobre as ferramentas e painéis utilizados pela Equipe de Planejamento Operacional.

        O objetivo principal é:
    Mapear e centralizar as ferramentas, painéis e boas práticas utilizadas.
    Armazenar automaticamente essas informações em um arquivo Excel versionado em um repositório GitHub.
    Facilitar o compartilhamento e análise posterior dessas informações.


🚀 Funcionalidades
✅ Formulário interativo para preenchimento:
Identificação do usuário.
Seleção dos painéis utilizados.
Comentários opcionais sobre cada painel.
Cadastro de múltiplas ferramentas, com informações detalhadas.
✅ Gerenciamento de múltiplos feedbacks:
Adição dinâmica de comentários para diferentes painéis.
✅ Cadastro de múltiplas ferramentas:
Nome, objetivo, tipo, categoria, importância e horas gastas.
✅ Validação automática:
Campos obrigatórios destacados com *.
Mensagens de erro para campos não preenchidos.
✅ Armazenamento automático no GitHub (explicação detalhada)
Este projeto implementa uma funcionalidade de armazenamento automático dos dados no GitHub, utilizando a GitHub REST API para realizar o versionamento do arquivo de dados.
    Como funciona?
Autenticação via Token Pessoal
A aplicação se autentica junto à API do GitHub usando um Personal Access Token (PAT) configurado no arquivo .streamlit/secrets.toml.
Esse token garante que apenas usuários autorizados consigam enviar atualizações ao repositório.
Leitura da Planilha de Dados

Antes de salvar um novo envio, a aplicação:
    Faz uma requisição GET para a API do GitHub.
    Obtém o conteúdo atual do arquivo .xlsx armazenado no repositório.
    Decodifica o conteúdo Base64 e carrega a planilha como um DataFrame (pandas).
    Atualização dos Dados
    Após o usuário preencher o formulário:
    Os novos dados são transformados em um DataFrame.
    A aplicação concatena os dados novos com os dados antigos, preservando o histórico.
    Versionamento do Arquivo
    Para salvar a atualização:
    O DataFrame atualizado é convertido novamente para arquivo .xlsx.
    O conteúdo binário do arquivo é codificado em Base64.
    A aplicação faz uma requisição PUT à API do GitHub, enviando o arquivo atualizado.
    A requisição inclui o parâmetro sha (identificador do estado atual do arquivo) para garantir que a atualização seja feita sobre a versão correta — isso evita conflitos e garante o versionamento controlado.

Resultado
    Cada envio de formulário gera automaticamente uma nova versão do arquivo de dados no repositório.
    O histórico completo dos envios fica preservado na aba "Commits" do repositório GitHub.
    Permite transparência, auditoria e colaboração entre múltiplos usuários.
Vantagens deste método:
✅ Não requer banco de dados adicional — usa o próprio GitHub como backend de armazenamento.
✅ Mantém o histórico completo — possibilita rollback para versões anteriores.
✅ Aumenta a segurança — via autenticação com token e controle de permissões do repositório.
✅ Facilita o deploy — pode rodar facilmente na Streamlit Cloud, sem necessidade de infra adicional.


✅ Confirmação de envio:
Mensagem de sucesso.
Link para upload de arquivos relacionados.
Resumo visual do que foi enviado.

🛠️ Tecnologias Utilizadas
Streamlit — Framework para criação de apps de dados.
Pandas — Manipulação e análise de dados.
Python Requests — Para integração com API do GitHub.
Pillow — Manipulação de imagens.
GitHub API — Para versionamento automático dos dados.
Base64 — Para codificação/decodificação de arquivos na comunicação com GitHub.

🖼️ Estrutura do Formulário
1. Identificação
Campo: E-mail MRV (obrigatório)
2. Seleção de Painéis
Lista de painéis utilizados pela equipe.
Opção de comentar sobre cada painel selecionado.
3. Cadastro de Ferramentas
Nome da ferramenta (obrigatório).
Objetivo (obrigatório).
Tipo (obrigatório): Power BI, Excel, Report e-mail, Power Point, Python ou Outra.
Categoria (obrigatório): Seleção pré-definida (Ex.: AUXÍLIO REGIONAL, MOP/EMP, etc.).
Importância (obrigatório): Muito importante, Importante, Pouco importante, Não importante.
Horas gastas mensalmente (obrigatório).

➡️ Possibilidade de adicionar várias ferramentas no mesmo envio.

🗂️ Estrutura do Projeto
bash
Copiar
Editar
├── app.py                # Arquivo principal da aplicação Streamlit
├── guia_lateral.py      # Módulo com função auxiliar para exibir guia lateral
├── logo_mrv_light.png   # Logo institucional
├── requirements.txt     # Dependências Python
├── .streamlit/
│   └── secrets.toml     # Configurações sensíveis (token, usuário GitHub etc.)
└── README.md            # Documentação do projeto


🔒 Configuração de Segredos (secrets.toml)
    Para integração com GitHub, é necessário configurar as credenciais no arquivo .streamlit/secrets.toml:
toml
Copiar
Editar
[github]
token = "SEU_TOKEN_PESSOAL"
username = "SEU_USERNAME_GITHUB"
repo = "NOME_DO_REPOSITORIO"
file_path = "CAMINHO/arquivo.xlsx"
branch = "main"

Streamlit Clound (app) -> Manage app -> Settings -> Secrets:
    [github]
    token = "digite seu token"
    username = "cleitonsouzamrv"
    repo = "pesquisa_PO"
    file_path = "base_dados_pesquisa_PO.xlsx"
    branch = "main"


⚙️ Como Executar o Projeto Localmente
    Clone o repositório:
bash
Copiar
Editar
git clone https://github.com/seuusuario/seurepositorio.git
cd seurepositorio
    Crie um ambiente virtual e ative:
bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
    Instale as dependências:
bash
Copiar
Editar
pip install -r requirements.txt
Configure as credenciais em .streamlit/secrets.toml.
    Execute o app:  
bash
Copiar
Editar
streamlit run app.py
    Acesse via navegador:
arduino
Copiar
Editar
http://localhost:8501


🌐 Deploy
O app pode ser facilmente publicado em:
Streamlit Cloud
Heroku
Servidores próprios
    Para deploy no Streamlit Cloud:
        Certifique-se de que o arquivo secrets.toml esteja configurado nas Secrets do projeto na plataforma.
✅ Checklist de Funcionamento
✔️ Autenticação via token do GitHub
✔️ Leitura de planilha .xlsx diretamente do repositório
✔️ Atualização do arquivo com novos envios
✔️ Interface responsiva para múltiplos inputs
✔️ Resumo das informações enviadas
✔️ Link para upload adicional de arquivos


🔗 Link para upload de ferramentas
Após o envio, o usuário será orientado a realizar o upload na pasta oficial:

👉 Clique aqui para acessar a pasta
https://mrvengenhariasa.sharepoint.com/sites/PlanejamentoEstratgicodeObra/Documentos%20Compartilhados/Forms/AllItems.aspx?id=%2Fsites%2FPlanejamentoEstratgicodeObra%2FDocumentos%20Compartilhados%2F10%2E%20Processos%20Automatizados%2FProjetos%20Python%2FProjeto%5FGPO%2FFerramentas%20%2D%20Planejamento%20Operacional&p=true&ga=1

🎯 Motivação do Projeto
    Padronizar a coleta de informações sobre as ferramentas utilizadas.
    Automatizar o versionamento dos dados.
    Facilitar a análise de produtividade e uso de recursos pela equipe de Planejamento Operacional.
    Promover transparência e eficiência na gestão de ferramentas.
    Apoiar a "Ponta" de modo a melhorar/desenvolver ferramentas funcionais para otimizar seu trabalho.

📞 Contato
Equipe de Planejamento Operacional — MRV&CO
Desenvolvido por: Cleiton Souza
E-mail: [cleiton.souza@mrv.com.br]

