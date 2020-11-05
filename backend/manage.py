import shlex
import subprocess
import pendulum
from flask_script import Manager
from seeds import ProgrammingLanguageSeeder
from main import app
from src.app.models import db

manager = Manager(app)


@manager.command
def test():
    print("test command: application manager works.")


@manager.command
def start_local_db():
    print('Starting local database: codelogue_db')
    startDbCmd = shlex.split('docker start codelogue_db')
    subprocess.run(startDbCmd)


@manager.command
def stop_local_db():
    print('Stopping local database: codelogue_db')
    startDbCmd = shlex.split('docker stop codelogue_db')
    subprocess.run(startDbCmd)


@manager.command
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def init_migration():
    print('Initializing database migration folder with contents.')
    initMigrationCmd = shlex.split('flask db init')
    subprocess.run(initMigrationCmd)


@manager.command
def apply_migration():
    time = pendulum.now().to_rfc822_string()
    print(f'Applying migration {time}')
    migrateCmd = shlex.split(f'flask db migrate =m"{time}"')
    subprocess.run(migrateCmd)


@manager.command
def upgrade_migration():
    print('Upgrading migration.')
    upgradeCmd = shlex.split("flask db upgrade")
    subprocess.run(upgradeCmd)


@manager.command
def seed_db():
    ProgrammingLanguageSeeder().run()


@manager.command
def start_server():
    app.run(host='0.0.0.0', threaded=True, debug=True, port=5001)


if __name__ == "__main__":
    manager.run()