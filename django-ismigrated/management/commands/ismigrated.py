# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from optparse import make_option
from importlib import import_module
from sys import exit

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.migrations.loader import MigrationLoader
from django.utils.module_loading import module_has_submodule


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database', default=DEFAULT_DB_ALIAS,
                    help='Nominates a database to check for migrations.' 'Defaults to the "default" database.'),
        )

    help = "Checks for un-applied migrations. Exits with a nonzero status code if there are."

    def handle(self, *args, **options):
        # This code is taken almost entirely from Django's migrate command.

        # From django.core.management.commands.migrate, in Command.handle

        # Import the 'management' module within each installed app, to register
        # dispatcher events.
        for app_config in apps.get_app_configs():
            if module_has_submodule(app_config.module, "management"):
                import_module('.management', app_config.name)

        # Get the database we're operating from
        db = options.get('database')
        connection = connections[db]


        # From django.core.management.commands.migrate, in Command.show_migration_list

        # Load migrations from disk/DB
        loader = MigrationLoader(connection, ignore_no_migrations=True)
        graph = loader.graph
        app_names = sorted(loader.migrated_apps)
        has_migrations = False
        for app_name in app_names:
            shown = set()
            for node in graph.leaf_nodes(app_name):
                for plan_node in graph.forwards_plan(node):
                    if plan_node not in shown and plan_node[0] == app_name:
                        if plan_node not in loader.applied_migrations:
                            has_migrations = True
                        shown.add(plan_node)

        if not has_migrations:
            print('Project is migrated')
        else:
            print('Project IS NOT migrated')

        # Exit 0 if there are no migrations, 1 otherwise.
        exit(int(has_migrations))
