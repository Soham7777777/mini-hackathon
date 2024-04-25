from Application import create_app
from instance import DevelopmentConfiguration

# debugging the application
if __name__ == '__main__':
    app = create_app(configClass=DevelopmentConfiguration)
    app.run(debug=True)