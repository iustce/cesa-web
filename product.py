from project import app
from project.application import configure_app
from project.config import ProductionConfig

configure_app(app, ProductionConfig())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
