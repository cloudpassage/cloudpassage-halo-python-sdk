"""HttpHelper class.  Primary-level object, facilitates
GET / POST / PUT / DELETE requests against API.
"""
import sys
import json
import urlparse
from cloudpassage.exceptions import CloudPassageValidation
from cloudpassage.exceptions import CloudPassageGeneral
import cloudpassage.utility as utility
import requests


class HttpHelper(object):
    """This class handles communication with the CloudPassage API.

    When instantiating this class, pass in a \
    :class:`cloudpassage.HaloSession` \
    object (referred to here as connection, as it defines connection \
    parameters for interacting with the API).

    """

    def __init__(self, connection):
        if self.python_version() < "2.7.10":
            err_msg = "Please make sure your python version is > 2.7.10"
            raise CloudPassageGeneral(err_msg)
        self.connection = connection

    def python_version(self):
        return sys.version.split(" ")[0]

    def get(self, endpoint, **kwargs):
        """This method performs a GET against Halo's API.

        It will attempt to authenticate using the credentials (required
        to instantiate the object) if the session has either:
        1) Not been authenticated yet
        2) OAuth Token has expired

        This is a primary method, meaning it reaches out directly to the Halo
        API, and should only be utilized by secondary methods with a more
        specific purpose, like gathering events from /v1/events.  If you're
        using this method because the SDK doesn't provide a more specific
        method, please reach out to toolbox@cloudpassage.com so we can get
        an enhancement request in place for you.

        Args:
            endpoint (str): URL- everything between \
            api.cloudpassage.com and any parameters to be passed. \
            Example: /v1/events

        Keyword Args:
            params (list of dict): This is a list of dictionary objects, \
            represented like this: [{"k1": "two,too"}] \
            which goes into the URL looking like this: ?k1=two,too. \
            If you use a list as the value in a dictionary here, you'll get \
            two k/v pairs represented in the URL and the CloudPassage API \
            doesn't operate like that.  Only the last instance of that \
            variable will be considered, and your results may be confusing.  \
            So don't do it.  Dictionaries should be {str:str}.
        """

        if self.connection.auth_token is None:
            self.connection.authenticate_client()
        prefix = self.connection.build_endpoint_prefix()
        url = prefix + endpoint
        headers = self.connection.build_header()
        if "params" in kwargs:
            response = requests.get(url, headers=headers,
                                    params=kwargs["params"])
        else:
            response = requests.get(url, headers=headers)
        success, exception = utility.parse_status(url, response.status_code,
                                                  response.text)
        if success is True:
            return response.json()

        # If we get a 401, it could be an expired key.  We retry once.
        if response.status_code == 401:
            self.connection.authenticate_client()
            headers = self.connection.build_header()
            if "params" in kwargs:
                response = requests.get(url, headers=headers,
                                        params=kwargs["params"])
            else:
                response = requests.get(url, headers=headers)
            success, exception = utility.parse_status(url,
                                                      response.status_code,
                                                      response.text)
            if success is True:
                return response.json()
        raise exception

    def get_paginated(self, endpoint, key, max_pages, **kwargs):
        """This method returns a concatenated list of objects
        from the Halo API.

        It's really a wrapper for the get() method.  Pass in the
        path as with the get() method, and a maxpages number.
        Maxpages is expected to be an integer between 2 and 100

        Args:
            endpoint (str): Path for initial query
            key (str): The key in the response containing the objects \
            of interest.  For instance, the /v1/events endpoint will \
            have the "events" key, which contains a list of dictionary \
            objects representing Halo events.
            maxpages (int): This is a number from 2-100.  More than 100 pages \
            can take quite a while to return, so beyond that you should \
            consider using this SDK as a component in a multi-threaded tool.
        Keyword Args:
            params (list of dict): This is a list of dictionary objects, \
            represented like this: [{"k1": "two,too"}] \
            which goes into the URL looking like this: ?k1=two,too . \
            If you use a list as the value in a dictionary here, you'll get \
            two k/v pairs represented in the URL and the CloudPassage API \
            doesn't operate like that.  Only the last instance of that \
            variable will be considered, and your results may be confusing.  \
            So don't do it.  Dictionaries should be {str:str}.

        """

        max_pages_valid, pages_invalid_msg = utility.verify_pages(max_pages)
        if not max_pages_valid:
            raise CloudPassageValidation(pages_invalid_msg)
        more_pages = False
        response_accumulator = []
        if "params" in kwargs and kwargs["params"] is not {}:
            initial_page = self.get(endpoint, params=kwargs["params"])
        else:
            initial_page = self.get(endpoint)
        response, next_page = self.process_page(initial_page, key)
        response_accumulator.extend(response)
        pages_parsed = 1
        if next_page is not None:
            more_pages = True
        while more_pages:
            page = self.get(next_page)
            response, next_page = self.process_page(page, key)
            response_accumulator.extend(response)
            pages_parsed += 1
            if next_page is None:
                more_pages = False
            if pages_parsed >= max_pages:
                more_pages = False
        return response_accumulator

    @classmethod
    def process_page(cls, page, key):
        """Page goes in, list data comes out."""
        response_accumulator = []
        next_page = None
        if key not in page:
            fail_msg = ("Requested key %s not found in page"
                        % key)
            raise CloudPassageValidation(fail_msg)
        for k in page[key]:
            response_accumulator.append(k)
        if "pagination" in page:
            if "next" in page["pagination"]:
                nextpage = page["pagination"]["next"]
                endpoint = str(urlparse.urlsplit(nextpage)[2] + "?" +
                               urlparse.urlsplit(nextpage)[3])
                next_page = endpoint
        return response_accumulator, next_page

    def post(self, endpoint, reqbody):
        """This method performs a POST against Halo's API.

        As with the GET method, it will attempt to (re)authenticate
        the session if the key is expired or has not yet been retrieved.

        Also like the GET method, it is not intended for direct use (though
        we won't stop you).  If you need something that the SDK doesn't
        already provide, please reach out to toolbox@cloudpassage.com and
        let us get an enhancement request submitted for you.

        Args:
            endpoint (str): path component of URL
            reqbody (dict): Dictionary to be converted to JSON for insertion \
            as payload for request.

        """

        if self.connection.auth_token is None:
            self.connection.authenticate_client()
        prefix = self.connection.build_endpoint_prefix()
        url = prefix + endpoint
        headers = self.connection.build_header()
        response = requests.post(url, headers=headers,
                                 data=json.dumps(reqbody))
        success, exception = utility.parse_status(url, response.status_code,
                                                  response.text)
        if success is False:
            # If we get a 401, it could be an expired key.  We retry once.
            if response.status_code == 401:
                self.connection.authenticate_client()
                headers = self.connection.build_header()
                response = requests.post(url, headers=headers,
                                         data=json.dumps(reqbody))
                success, exception = utility.parse_status(url,
                                                          response.status_code,
                                                          response.text)
                if success is True:
                    return response.json()
            raise exception
        else:
            return response.json()

    def put(self, endpoint, reqbody):
        """This method performs a PUT against Halo's API.

        As with the GET method, it will attempt to (re)authenticate
        the session if the key is expired or has not yet been retrieved.

        Also like the GET method, it is not intended for direct use (though
        we won't stop you).  If you need something that the SDK doesn't
        already provide, please reach out to toolbox@cloudpassage.com and
        let us get an enhancement request submitted for you.

        Args:
            endpoint (str): Path component of URL

        """

        if self.connection.auth_token is None:
            self.connection.authenticate_client()
        prefix = self.connection.build_endpoint_prefix()
        url = prefix + endpoint
        headers = self.connection.build_header()
        response = requests.put(url, headers=headers,
                                data=json.dumps(reqbody))
        success, exception = utility.parse_status(url, response.status_code,
                                                  response.text)
        if success is False:
            # If we get a 401, it could be an expired key.  We retry once.
            if response.status_code == 401:
                self.connection.authenticate_client()
                headers = self.connection.build_header()
                response = requests.put(url, headers=headers,
                                        data=json.dumps(reqbody))
                success, exception = utility.parse_status(url,
                                                          response.status_code,
                                                          response.text)
                if success is True:
                    return response.json()
            raise exception
        else:
            # Sometimes we don't get json back...
            try:
                return_value = response.json()
            except ValueError:
                return_value = response.text
            return return_value

    def delete(self, endpoint, **kwargs):
        """This method performs a Delete against Halo's API.

        It will attempt to authenticate using the credentials (required
        to instantiate the object) if the session has either:
        1) Not been authenticated yet
        2) OAuth Token has expired

        This is a primary method, meaning it reaches out directly to the Halo
        API, and should only be utilized by secondary methods with a more
        specific purpose, like gathering events from /v1/events.  If you're
        using this method because the SDK doesn't provide a more specific
        method, please reach out to toolbox@cloudpassage.com so we can get
        an enhancement request in place for you.

        Args:
            endpoint (str): Path component of URL

        """

        if self.connection.auth_token is None:
            self.connection.authenticate_client()
        prefix = self.connection.build_endpoint_prefix()
        url = prefix + endpoint
        headers = self.connection.build_header()
        if "params" in kwargs:
            response = requests.delete(url, headers=headers,
                                       params=kwargs["params"])
        else:
            response = requests.delete(url, headers=headers)
        success, exception = utility.parse_status(url, response.status_code,
                                                  response.text)
        if success is False:
            # If we get a 401, it could be an expired key.  We retry once.
            if response.status_code == 401:
                self.connection.authenticate_client()
                headers = self.connection.build_header()
                response = requests.delete(url, headers=headers)
                success, exception = utility.parse_status(url,
                                                          response.status_code,
                                                          response.text)
                if success is True:
                    return response.json()
            raise exception
        else:
            # Sometimes we don't get json back...
            try:
                return_value = response.json()
            except ValueError:
                return_value = response.text
            return return_value
