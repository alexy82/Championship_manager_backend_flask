import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app
from app.core.models import db

application = create_app()

manager = Manager(application)

migrate = Migrate(application, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    application.run(debug=os.getenv('DEBUG'))


@manager.command
def test_command():
    print('Hello World')


if __name__ == '__main__':
    manager.run()
