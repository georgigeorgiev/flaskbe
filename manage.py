#!/usr/bin/env python
import imp
import subprocess
import sys
import time
from flask_script import Manager
from migrate.versioning import api
import config as config_module

from flaskbe import db, create_app
import os

manager = Manager(create_app)


@manager.command
def dbcreate(config='development'):
    """Creates the database."""
    config_cls = config_module.config[config]

    db.create_all()
    time.sleep(1)
    if not os.path.exists(config_cls.SQLALCHEMY_MIGRATE_REPO):
        api.create(config_cls.SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(config_cls.SQLALCHEMY_DATABASE_URI, config_cls.SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(config_cls.SQLALCHEMY_DATABASE_URI,
                            config_cls.SQLALCHEMY_MIGRATE_REPO,
                            api.version(config_cls.SQLALCHEMY_MIGRATE_REPO))


@manager.command
def dbmigrate(config='development'):
    """Creates database migration and migrate the database."""
    config_cls = config_module.config[config]

    v = api.db_version(config_cls.SQLALCHEMY_DATABASE_URI,
                       config_cls.SQLALCHEMY_MIGRATE_REPO)
    migration = config_cls.SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(config_cls.SQLALCHEMY_DATABASE_URI, config_cls.SQLALCHEMY_MIGRATE_REPO)
    exec(old_model, tmp_module.__dict__)
    script = api.make_update_script_for_model(config_cls.SQLALCHEMY_DATABASE_URI, config_cls.SQLALCHEMY_MIGRATE_REPO,
                                              tmp_module.meta, db.metadata)
    open(migration, "wt").write(script)
    api.upgrade(config_cls.SQLALCHEMY_DATABASE_URI, config_cls.SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(config_cls.SQLALCHEMY_DATABASE_URI, config_cls.SQLALCHEMY_MIGRATE_REPO)
    print('New migration saved as ' + migration)
    print('Current database version: ' + str(v))


@manager.command
def dbupgrade(config='development'):
    """Upgrade database to higher revision."""
    config_cls = config_module.config[config]

    api.upgrade(config_cls.SQLALCHEMY_DATABASE_URI, config_cls.SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(config_cls.SQLALCHEMY_DATABASE_URI, config_cls.SQLALCHEMY_MIGRATE_REPO)
    print('Current database version: ' + str(v))


@manager.command
def dbdowngrade(config='development'):
    """Upgrade database to higher revision."""
    config_cls = config_module.config[config]

    v = api.db_version(config_cls.SQLALCHEMY_DATABASE_URI, config_cls.SQLALCHEMY_MIGRATE_REPO)
    api.downgrade(config_cls.SQLALCHEMY_DATABASE_URI, config_cls.SQLALCHEMY_MIGRATE_REPO, v - 1)
    v = api.db_version(config_cls.SQLALCHEMY_DATABASE_URI, config_cls.SQLALCHEMY_MIGRATE_REPO)
    print('Current database version: ' + str(v))


@manager.command
def test():
    """Runs unit tests."""
    tests = subprocess.call(['python', '-c', 'import tests; tests.run()'])
    sys.exit(tests)


if __name__ == '__main__':
    manager.run()
