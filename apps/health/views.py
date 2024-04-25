import json
from collections import OrderedDict
from importlib import import_module

from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

HEARTBEAT = {
    'checkers': [
        'apps.health.checkers.health_redis_cache',
        'apps.health.checkers.health_database',
    ]
}


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        response: dict = {}
        status = 400
        for checker in HEARTBEAT['checkers']:
            checker_module = import_module(checker)
            checker_name = checker_module.__name__.split('.')[-1]
            data = checker_module.check(request)
            response[checker_name] = data
        data = OrderedDict(sorted(response.items()))
        # set response status
        if response.get('health_database') is not None and response.get('health_database').get(
                'default'):
            status = 200
        return HttpResponse(
            json.dumps(data),
            content_type="application/json",
            status=status
        )
