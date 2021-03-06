import logging
import traceback

from django.conf import settings
from django.db import connection
from django.db import OperationalError
from django.http import HttpResponseNotAllowed
from django.template import loader
from django.middleware.locale import LocaleMiddleware
from django.utils.translation import ugettext as _
from django.utils.translation.trans_real import parse_accept_lang_header
from multidb.pinning import use_master


class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)


class ExceptionLoggingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_exception(self, request, exception):
        print(traceback.format_exc())


class HTTPResponseNotAllowedMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, HttpResponseNotAllowed):
            response.content = loader.render_to_string(
                "405.html", request=request)

        return response


class LocaleMiddlewareWithTweaks(LocaleMiddleware):
    """
    Overrides LocaleMiddleware from django with:
        Khmer `km` language code in Accept-Language is rewritten to km-kh
    """

    def process_request(self, request):
        accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        try:
            codes = [code for code, r in parse_accept_lang_header(accept)]
            if 'km' in codes and 'km-kh' not in codes:
                request.META['HTTP_ACCEPT_LANGUAGE'] = accept.replace('km',
                                                                      'km-kh')
        except Exception as e:
            # this might fail if i18n is disabled.
            logging.exception(_(u'Settings request META HTTP accept language '
                                'threw exceptions: %s' % str(e)))

        super(LocaleMiddlewareWithTweaks, self).process_request(request)


class SqlLogging(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        from sys import stdout
        if stdout.isatty():
            for query in connection.queries:
                print("\033[1;31m[%s]\033[0m \033[1m%s\033[0m" % (
                    query['time'], " ".join(query['sql'].split())))

        return response


class OperationalErrorMiddleware(BaseMiddleware):
    """
    Captures requests returning 500 status code.
    Then retry it against master database.
    """
    def process_exception(self, request, exception):
        # Filter out OperationalError Exceptions
        if isinstance(exception, OperationalError):
            already_raised = getattr(settings, "ALREADY_RAISED", False)
            message = "canceling statement due to conflict with recovery"
            if message in str(exception):
                if not already_raised:
                    settings.ALREADY_RAISED = True
                    with use_master:
                        response = self.get_response(request)
                        return response
                settings.ALREADY_RAISED = False
