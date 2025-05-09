from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Importa e registra rotas
    from app.routes import painel, form
    app.register_blueprint(painel.bp)
    app.register_blueprint(form.bp)

    return app
