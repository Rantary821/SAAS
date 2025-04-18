from flask import Blueprint, render_template, request

bp = Blueprint('preencher', __name__)

@bp.route('/preencher-projeto', methods=['GET', 'POST'])
def preencher_projeto():
    if request.method == 'POST':
        # Aqui você processa os dados do formulário depois
        print(request.form)
    return render_template('preencher_projeto.html')
