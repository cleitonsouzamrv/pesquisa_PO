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
