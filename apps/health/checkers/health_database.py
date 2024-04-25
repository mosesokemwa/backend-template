from collections import OrderedDict

from django.db import OperationalError, connections


def check(request):
    """Check the database connections using the django DATABASES settings
    and return OK if the connection is established.
    """
    return {
        db: get_connection_info(connections[db])['version']
        for db in connections
    }


def get_connection_info(connection):
    connection_info = OrderedDict()

    engine = connection.settings_dict.get('ENGINE')

    connection_info['alias'] = connection.alias
    connection_info['name'] = connection.settings_dict.get('NAME')
    connection_info['engine'] = engine
    connection_info['version'] = get_database_version(connection, engine)
    connection_info['host'] = connection.settings_dict.get('HOST')
    connection_info['port'] = connection.settings_dict.get('PORT')
    return connection_info


def get_database_version(connection, engine):
    if connection.settings_dict['ENGINE'] == 'django.db.backends.dummy':
        return
    engines = {
        'django.db.backends.postgresql': 'SELECT version();',
        'django.db.backends.postgresql_psycopg2': 'SELECT version();',
        'django.db.backends.mysql': 'SELECT version();',
        'django.db.backends.sqlite3': 'select sqlite_version();',
        'django.db.backends.oracle': 'select * from v$version;',
        'django.contrib.gis.db.backends.mysql': 'SELECT version();',
        'django.contrib.gis.db.backends.postgis': 'SELECT version();',
        'django.contrib.gis.db.backends.spatialite': (
            'select sqlite_version();'
        ),
        'django.contrib.gis.db.backends.oracle': 'select * from v$version;',
    }
    query = engines[engine]
    return execute_sql(connection, query)


def execute_sql(connection, stmt):
    try:
        cursor = connection.cursor()
    except OperationalError as e:
        # return {'error': str(e)} # enable this for a more detailed response
        return False

    cursor.execute(stmt)
    results = cursor.fetchone()[0]
    # return results # enable this for a more detailed response
    return True
