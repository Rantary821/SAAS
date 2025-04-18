from app import create_app
import logging
from logging.handlers import RotatingFileHandler
import os

app = create_app()

if __name__ == '__main__':
        # Garante que o diretório de logs existe
    os.makedirs("logs", exist_ok=True)

    # Cria handler para arquivo com rotação (evita logs gigantes)
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=5 * 1024 * 1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    # Formato detalhado do log
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s] %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)

    # Aplica a todos os loggers da aplicação
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().addHandler(file_handler)

    # Flask logger usa 'werkzeug' para as requisições HTTP
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').addHandler(file_handler)

    # Logger da própria app
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

    # Teste opcional de log
    app.logger.info("Servidor Flask iniciado.")
    app.run(host='0.0.0.0', port=5000, debug=True)
