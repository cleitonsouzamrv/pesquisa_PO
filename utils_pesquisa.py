import re

def extrair_info_painel(texto):
    """
    Extrai o nome, o comentário após {'comentario': '...'} e a nota após 'nota':.
    Exclusivo para Painel.
    """
    nome = texto.split(':')[0].strip()
    
    comentario = None
    nota = None

    comentario_match = re.search(r"\{'comentario':\s*'(.*?)'", texto)
    if comentario_match:
        comentario = comentario_match.group(1).strip()

    nota_match = re.search(r"'nota':\s*([0-9\.]+)", texto)
    if nota_match:
        nota = nota_match.group(1).strip()

    return nome, comentario, nota

def desmembrar_ferramenta(texto):
    """
    Desmembra a string concatenada da ferramenta em:
    Nome, Objetivo, Tipo, Categoria, Importância, Horas.
    """
    partes = [parte.strip() for parte in texto.split('_')]
    return {
        'Ferramenta - Nome': partes[0] if len(partes) > 0 else '',
        'Ferramenta - Objetivo': partes[1] if len(partes) > 1 else '',
        'Ferramenta - Tipo': partes[2] if len(partes) > 2 else '',
        'Ferramenta - Categoria': partes[3] if len(partes) > 3 else '',
        'Ferramenta - Importância': partes[4] if len(partes) > 4 else '',
        'Ferramenta - Horas gastas mensais': partes[5] if len(partes) > 5 else ''
    }

