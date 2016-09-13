#!/usr/bin/env python
import subprocess
import sys
from flask_script import Manager

from flaskbe import db, create_app

manager = Manager(create_app)


@manager.command
def createdb(drop_first=False):
    """Creates the database."""
    pass
    # if drop_first:
    #     db.drop_all()
    # db.create_all()


@manager.command
def test():
    """Runs unit tests."""
    tests = subprocess.call(['python', '-c', 'import tests; tests.run()'])
    sys.exit(tests)


if __name__ == '__main__':
    manager.run()
