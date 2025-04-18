from flask import Blueprint, render_template, request
import xml.etree.ElementTree as ET
import os

bp = Blueprint('form', __name__)

@bp.route('/preencher-projeto', methods=['GET'])
def gerar_formulario():
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

    return render_template('form.html', modulos=modulos, inversores=inversores)


@bp.route('/cadastro-modulo')
def cadastro_modulo():
    return render_template('cadastro_modulo.html')


@bp.route('/cadastro-inversor')
def cadastro_inversor():
    return render_template('cadastro_inversor.html')
