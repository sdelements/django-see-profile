import cProfile
import logging
import pstats
import sqlparse
from io import StringIO

from django.core.exceptions import MiddlewareNotUsed
from django.db import connection

from security.middleware import BaseMiddleware


class ProfilingMiddleware(BaseMiddleware):
    """
    Adds the ability to profile requests via a header.

    Usage:
    Add the middleware to the MIDDLEWARE list. New boolean setting
    "ENABLE_PROFILING" will be required to be set in the settings file. When
    set to False, the middleware will deactivate itself. When set to True, the
    middleware will be active.

    When the middleware is active, it will log the data for any request that
    supplies the X-Profile header in the HTTP request. This data will be logged
    to the 'profiling' logger, so in order to see the results of this profiling
    the Django logging will need to configure handlers for the 'profiling'
    logger. Profiling will be configured at the DEBUG level.
    """

    REQUIRED_SETTINGS = ('ENABLE_PROFILING', 'DEBUG')
    request_separator = f"\n{'=' * 80}\n"
    query_separator = f"\n{'*' * 80}\n"

    def __init__(self, get_response=None):
        super().__init__(get_response)
        if not self.enable_profiling:
            raise MiddlewareNotUsed()
        self.logger = logging.getLogger('profiling')

    def load_setting(self, setting, value):
        setattr(self, setting.lower(), value)

    def format_queries(self, queries):
        return self.query_separater.join(
            sqlparse.format(query['sql'], reindent=True, keyword_case='upper')
            for query in queries
        )

    def __call__(self, request):
        # Only profile requests that have a 'X-Profile' HTTP header
        if 'HTTP_X_PROFILE' not in request.META:
            return self.get_response(request)

        out = StringIO()
        out.write(self.request_separator)

        # Add method & path info to differentiate requests
        out.write(
            f"{request.method} {request.path}"
        )

        # We can only profile queries in debug mode
        if self.debug:
            num_previous_queries = len(connection.queries)

        # Begin collecting time profiling data
        profile = cProfile.Profile()
        profile.enable()

        # Continue down the middleware chain
        response = self.get_response(request)

        # Get the profile stats & pull out the top cumulative & total time
        # data
        profile_stats = pstats.Stats(profile, stream=out)
        profile_stats = profile_stats.sort_stats('cumulative')
        profile_stats.print_stats(128)
        profile_stats.sort_stats("tottime")
        profile_stats.print_stats(15)

        # Print out our queries
        if self.debug:
            query_count = len(connection.queries) - num_previous_queries
            out.write(f"\n{query_count} Queries:\n")
            queries = connection.queries[num_previous_queries:]
            out.write(self.format_queries(queries))

        out.write(self.request_separator)
        self.logger.debug(out.getvalue())

        return response
