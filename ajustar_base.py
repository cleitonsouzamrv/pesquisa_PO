import pandas as pd

# Caminho para a planilha original
arquivo = 'base_dados_pesquisa_PO.xlsx'

# Carrega a planilha
df = pd.read_excel(arquivo)

# Função para ajustar a string
def ajustar_ferramenta(ferramentas_str):
    if pd.isnull(ferramentas_str):
        return ferramentas_str
    # Ajusta cada ferramenta separadamente
    ferramentas = ferramentas_str.split(';')
    ferramentas_ajustadas = []
    for ferramenta in ferramentas:
        if ferramenta.strip() == '':
            continue
        # Só ajusta se ainda tiver ','
        if ',' in ferramenta:
            ferramenta_ajustada = ferramenta.replace(',', '_')
            ferramentas_ajustadas.append(ferramenta_ajustada)
        else:
            ferramentas_ajustadas.append(ferramenta)
    return ';'.join(ferramentas_ajustadas)

# Aplica a função na coluna "Ferramentas"
df['Ferramentas'] = df['Ferramentas'].apply(ajustar_ferramenta)

# Salva como nova planilha
novo_arquivo = 'base_dados_pesquisa_PO_ajustada.xlsx'
df.to_excel(novo_arquivo, index=False)

print(f"✅ Ajuste concluído! Arquivo salvo como '{novo_arquivo}'")
