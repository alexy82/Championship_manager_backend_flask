import logging

from app.core.manager.token import get_info_token

logger = logging.getLogger('main')


def get_client_ip(request):
    try:
        if request.headers.getlist("X-Forwarded-For"):
            x_forwarded_for = request.headers.getlist('X-Forwarded-For')[0]
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.remote_addr
        return ip
    except:
        return None


def log_api_request(request):
    ip = get_client_ip(request)
    logger.info('Request | ip: {} | url: {} | method: {} | payload: {}'.format(
        ip,
        request.full_path,
        request.method,
        request.data
    ))
