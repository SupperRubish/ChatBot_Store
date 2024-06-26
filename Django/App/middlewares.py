from django.utils.deprecation import MiddlewareMixin


class Cros(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = '*'
        response['Access-Control-Allow-Credentials'] = True
        return response

