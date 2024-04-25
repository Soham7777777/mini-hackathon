# production enviornment, with no debug mode
from Application import create_app
from instance import DeploymentConfiguration

if __name__ == '__main__':
    app = create_app(configClass=DeploymentConfiguration)
    app.run()