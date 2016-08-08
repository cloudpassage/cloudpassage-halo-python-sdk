"""Event class"""


import cloudpassage.utility as utility
from cloudpassage.http_helper import HttpHelper


class Event(object):
    """Initializing the Event class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    # pylint: disable=too-few-public-methods
    # This cannot be combined with any other module, and still make sense

    def __init__(self, session):
        self.session = session
        self.supported_search_fields = [
            "group_id",
            "server_id",
            "server_platform",
            "critical",
            "type",
            "since",
            "until",
            "pages"
        ]
        return None

    def list_all(self, pages, **kwargs):
        """Returns a list of all events.


        Default filter returns ALL events.  This is a very verbose \
        and time-consuming operation.

        Args:
            pages (int): Max number of pages (of ten items each) to retrieve

        Keyword Args:
            group_id (list or str): A list or comma-separated string \
            containing the group IDs to retrieve events for.
            server_id (list or str): A list or comma-separated string \
            containing the server IDs to retrieve events for.
            server_platform (str): (linux | windows)
            type (list or str): A list or comma-separated string containing \
            the event types to query for.  A complete list of event types is \
            available \
            `here: <https://support.cloudpassage.com/entries/23125117-Events\
            #event-types>`_
            since (str): ISO 8601 formatted string representing the starting \
            date and time for query
            until (str): ISO 8601 formatted string representing the ending \
            date and time for query

        Returns:
            list: List of dictionary objects describing servers

        """

        endpoint = "/v1/events"
        key = "events"
        max_pages = pages
        request = HttpHelper(self.session)
        params = utility.assemble_search_criteria(self.supported_search_fields,
                                                  kwargs)
        response = request.get_paginated(endpoint, key, max_pages,
                                         params=params)
        return response
