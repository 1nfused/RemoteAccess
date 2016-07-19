import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from main import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

#Here we create a migrate instance with app and db as arguments
migrate = Migrate(app, db)
manager = Manager(app)


#Here we add a db command to manager, so we can run migrations from the
#command line
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
