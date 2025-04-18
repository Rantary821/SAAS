from flask import Blueprint, render_template, request, redirect, url_for
import xml.etree.ElementTree as ET
import os
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename

from app.utils.geolocalizacao import buscar_coordenadas_por_endereco
from app.utils.xml_utils import adicionar_modulo, adicionar_inversor
from app.utils.utils_excel import preencher_anexo_f

bp = Blueprint('form', __name__)

@bp.route('/preencher-projeto', methods=['GET', 'POST'])
def preencher_projeto():
    modulos, inversores = [], []
    try:
        tree = ET.parse('static/dados_padrao.xml')
        root = tree.getroot()

        for m in root.findall('./modulos/modulo'):
            modulos.append({k: m.findtext(k) for k in ('fabricante', 'modelo', 'potencia')})

        for i in root.findall('./inversores/inversor'):
            inversores.append({k: i.findtext(k) for k in ('fabricante', 'modelo', 'potencia')})

    except Exception as e:
        print(f"Erro ao carregar XML: {e}")

    # Inicializa para evitar erro no GET
    latitude = ''
    longitude = ''

    if request.method == 'POST':
        form = request.form

        nome = form.get('nome')
        cpf = form.get('cpf')
        celular = form.get('celular')
        email = form.get('email')
        codigo_uc = form.get('codigo_uc')
        cep = form.get('cep')
        rua = form.get('rua')
        numero = form.get('numero')
        bairro = form.get('bairro')
        cidade = form.get('cidade')
        estado = form.get('estado')
        latitude = form.get('latitude')
        longitude = form.get('longitude')

        # Se lat/lng estiverem vazios, tenta buscar automaticamente
        if not latitude or not longitude:
            latitude, longitude = buscar_coordenadas_por_endereco(
                rua, numero, bairro, cidade, estado
            )

        data_operacao = form.get('data_operacao')

        inv_fabricante = form.get('inv_fabricante')
        inv_modelo = form.get('inv_modelo')
        inv_potencia = form.get('inv_potencia')
        inv_quantidade = form.get('inv_quantidade')

        mod_fabricante = form.get('mod_fabricante')
        mod_modelo = form.get('mod_modelo')
        mod_potencia = form.get('mod_potencia')
        mod_quantidade = form.get('mod_quantidade')

        # Criação da pasta
        data_formatada = datetime.now().strftime('%Y-%m-%d')
        nome_pasta = f"{nome.lower().replace(' ', '_')}_{data_formatada}"
        caminho = Path('gerados') / estado / cidade / nome_pasta
        os.makedirs(caminho, exist_ok=True)

        # Salvar certificado do inversor (opcional)
        arquivo_certificado = request.files.get('inv_certificado')
        if arquivo_certificado and arquivo_certificado.filename:
            nome_arquivo = secure_filename(arquivo_certificado.filename)
            arquivo_certificado.save(caminho / nome_arquivo)

        # Gera planilha Anexo F
        endereco_completo = f"{rua}, {numero} - {bairro}"
        preencher_anexo_f(
            modelo_path='static/modelo_anexo_f.xlsx',  # atualize conforme seu modelo
            saida_path=str(caminho / 'anexo_f.xlsx'),
            nome=nome,
            cpf=cpf,
            telefone=celular,
            email=email,
            endereco=endereco_completo,
            cidade=cidade,
            latitude=latitude,
            longitude=longitude,
            data_operacao=data_operacao,
            qnt_mod=mod_quantidade,
            fab_mod=mod_fabricante,
            mod_mod=mod_modelo,
            qnt_inv=inv_quantidade,
            fab_inv=inv_fabricante,
            mod_inv=inv_modelo,
            pot_mod=mod_potencia,
            pot_inv=inv_potencia,
            pot_total="0",  # será ajustado na planilha
            padrao="B1",  # opcional
            forma_conexao="Aérea",  # opcional
            uc=codigo_uc,
            cep=cep
        )

        return redirect(url_for('painel.painel'))

    # No GET ou erro, retorna o template
    return render_template(
        'preencher_projeto.html',
        modulos=modulos,
        inversores=inversores,
        lat=latitude,
        lng=longitude
    )
