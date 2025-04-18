from flask import Blueprint, render_template, send_file
from pathlib import Path
import os
import zipfile
import io

bp = Blueprint('painel', __name__)

@bp.route('/')
def painel():
    projetos = carregar_estrutura_projetos()
    return render_template("base.html", projetos=projetos)

@bp.route('/painel-conteudo')
def painel_conteudo():
    projetos = carregar_estrutura_projetos()
    return render_template("painel_conteudo.html", projetos=projetos)

@bp.route('/gerar', methods=['POST'])
def gerar_tudo_zip():
    base_path = Path('gerados')

    if not base_path.exists():
        return "Nenhum projeto gerado encontrado.", 404

    memory_file = io.BytesIO()

    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, base_path)
                zipf.write(full_path, arcname=relative_path)

    memory_file.seek(0)

    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='projetos_gerados.zip'
    )

# === Função auxiliar ===
def carregar_estrutura_projetos():
    projetos = {}
    base_path = Path('gerados')
    if not base_path.exists():
        return {}

    for estado_dir in base_path.iterdir():
        if estado_dir.is_dir():
            estado = estado_dir.name
            projetos[estado] = {}
            for cidade_dir in estado_dir.iterdir():
                if cidade_dir.is_dir():
                    cidade = cidade_dir.name
                    projetos[estado][cidade] = []
                    for cliente_dir in cidade_dir.iterdir():
                        if cliente_dir.is_dir():
                            cliente_nome = cliente_dir.name
                            arquivos = []
                            for arq in cliente_dir.iterdir():
                                if arq.is_file():
                                    arquivos.append({
                                        "nome": arq.name,
                                        "caminho": str(arq)
                                    })
                            projetos[estado][cidade].append({
                                "nome": cliente_nome,
                                "arquivos": arquivos
                            })
    return projetos
