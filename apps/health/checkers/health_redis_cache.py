from django.conf import settings

try:
    import redis
    from redis.exceptions import ConnectionError
except ImportError:
    pass


def check(request):
    """
    Check the cache connection using the django CACHES settings
    """
    # if location has port number, it will be in the format redis://<host>:<port>
    location = settings.CACHES['default'].get('LOCATION', 'localhost')
    host = location.split('//')[-1].split(':')[0] if '://' in location else location.split(':')[0]
    port = location.split(':')[-1] if ':' in location else 6379
    db = settings.CACHES['default'].get('DB', 0)
    socket_timeout = settings.CACHES['default'].get('SOCKET_TIMEOUT', 0.1)

    try:
        redis_con = redis.StrictRedis(
            host=host, port=port, db=db, socket_timeout=socket_timeout)
        ping = redis_con.ping()
    except NameError:
        return {'error': 'cannot import redis library'}
    except ConnectionError as e:
        # uncomment below line to get a more detailed response
        # return {'error': str(e),'message': 'Redis server is not running'}
        return False

    # uncomment below object to get a more detailed response
    # return {
    #     'ping': ping,
    #     'version': redis_con.info().get('redis_version'),
    #     'cache hits': redis_con.info().get('keyspace_hits')
    #     }
    return True
