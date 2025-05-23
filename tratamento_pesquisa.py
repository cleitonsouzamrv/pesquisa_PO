import time
import pandas as pd
import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils_pesquisa import extrair_info_painel, desmembrar_ferramenta

LOG_FILE = 'tratamento_log.txt'

COL_EMAIL = 'E-mail MRV'
COL_DATA = 'Data/Hora do Envio'
COL_PAINEIS = 'Painéis'
COL_FERRAMENTAS = 'Ferramentas'

def registrar_log(mensagem):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{mensagem}\n")

def tratar_base(input_file='base_dados_pesquisa_PO.xlsx', 
                output_dir='.', 
                base_output_name='modelo_base_dados_tratada'):
    print(f"🔄 Detectada atualização. Iniciando tratamento...")

    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"⚠️ Erro ao ler a planilha: {e}")
        registrar_log(f"{datetime.now()} - ERRO ao ler a planilha: {e}")
        return

    registros_tratados = []

    for idx, row in df.iterrows():
        email = row[COL_EMAIL]
        data = row[COL_DATA]

        # Painéis
        paineis_raw = str(row.get(COL_PAINEIS, '')).split(';')
        for painel_item in paineis_raw:
            if painel_item.strip() == '':
                continue
            nome, comentario, nota = extrair_info_painel(painel_item)
            registros_tratados.append({
                'E-mail': email,
                'Data': data,
                'Tipo': 'Painel',
                'Nome': nome,
                'Comentário': comentario,
                'Nota': nota,
                'Ferramenta - Nome': '',
                'Ferramenta - Objetivo': '',
                'Ferramenta - Tipo': '',
                'Ferramenta - Categoria': '',
                'Ferramenta - Importância': '',
                'Ferramenta - Horas gastas mensais': ''
            })

        # Ferramentas
        ferramentas_raw = str(row.get(COL_FERRAMENTAS, '')).split(';')
        for ferramenta_item in ferramentas_raw:
            if ferramenta_item.strip() == '':
                continue

            f_partes = desmembrar_ferramenta(ferramenta_item)

            registros_tratados.append({
                'E-mail': email,
                'Data': data,
                'Tipo': 'Ferramenta',
                'Nome': f_partes['Ferramenta - Nome'],
                'Comentário': '',
                'Nota': '',
                **f_partes
            })

    df_tratado = pd.DataFrame(registros_tratados)

    final_file = os.path.join(output_dir, f"{base_output_name}.xlsx")

    try:
        df_tratado.to_excel(final_file, index=False)
        print(f'✅ Base tratada salva em: {final_file}')

        log_msg = f"{datetime.now()} - Tratamento concluído: {final_file} - {len(df_tratado)} registros"
        registrar_log(log_msg)
    except Exception as e:
        print(f"⚠️ Erro ao salvar a planilha tratada: {e}")
        registrar_log(f"{datetime.now()} - ERRO ao salvar a planilha tratada: {e}")

class MonitorHandler(FileSystemEventHandler):
    def __init__(self, input_file, output_dir, base_output_name):
        super().__init__()
        self.input_file = input_file
        self.output_dir = output_dir
        self.base_output_name = base_output_name

    def on_modified(self, event):
        if not event.is_directory and os.path.basename(self.input_file) in event.src_path:
            tratar_base(self.input_file, self.output_dir, self.base_output_name)

if __name__ == "__main__":
    input_file = 'base_dados_pesquisa_PO.xlsx'
    output_dir = '.'
    base_output_name = 'modelo_base_dados_tratada'

    path = os.path.dirname(os.path.abspath(input_file)) or '.'
    event_handler = MonitorHandler(input_file, output_dir, base_output_name)
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)

    print("🚀 Monitorando alterações na base de dados...")
    print(f"📂 Pasta monitorada: {path}")
    print(f"📄 Arquivo monitorado: {input_file}")
    print(f"📝 Log: {os.path.abspath(LOG_FILE)}")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("🛑 Monitoramento encerrado.")

    observer.join()
