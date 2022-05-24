"""General utilities"""
import json
import datetime
import os
import re
import sys
from .exceptions import CloudPassageValidation
from .exceptions import CloudPassageAuthentication
from .exceptions import CloudPassageAuthorization
from .exceptions import CloudPassageResourceExistence
from .exceptions import CloudPassageGeneral
from .exceptions import CloudPassageRateLimit
from distutils.version import LooseVersion
from .sanity import is_it_a_string


class Utility(object):
    @classmethod
    def determine_policy_metadata(cls, policy):
        """Return dict of policy type, name, and target platform.

        If string, attempts to convert to dict to parse.
        Possible return values for policy_type:
        CSM      -- Configuration Security Monitoring
        FIM      -- File Integrity Monitoring
        LIDS     -- Log Intrusion Detection System
        Firewall -- Firewall Policy
        None     -- Unable to determine poolicy type

        Possible return values for target_platform:
        Windows
        Linux
        None

        Example:
        determine_policy_type(string_from_file)
        {"policy_type": "CSM",
         "policy_name": "Test policy",
         "target_platform": "Windows"}

        Args:
            policy (str or dict): Policy in string or dict form.

        Returns:
            dict
        """

        working_pol = None
        return_body = {"policy_type": None,
                       "policy_name": None,
                       "target_platform": None}
        if is_it_a_string(policy):
            working_pol = json.loads(policy)
        elif isinstance(policy, dict):
            working_pol = policy.copy()
        else:
            print("Policy type must be str or dict, not %s!" % type(policy))
        try:
            derived_module_type = list(working_pol.items())[0][1]["module"]
            if derived_module_type == "fim":
                return_body["policy_type"] = "FIM"
            if derived_module_type == "csm":
                return_body["policy_type"] = "CSM"
            if derived_module_type == "lids":
                return_body["policy_type"] = "LIDS"
            if derived_module_type == "fw":
                return_body["policy_type"] = "Firewall"
        except AttributeError:
            pass
        try:
            return_body["policy_name"] = list(working_pol.items())[0][1]["name"]  # NOQA
        except AttributeError:
            pass
        try:
            derived_platform = list(working_pol.items())[0][1]["platform"]
            if derived_platform == 'linux':
                return_body["target_platform"] = 'Linux'
            elif derived_platform == 'windows':
                return_body["target_platform"] = 'Windows'
        except AttributeError:
            pass
        return return_body

    @classmethod
    def assemble_search_criteria(cls, supported_search_fields, arguments):
        """Verifies request params and returns a dict of validated arguments"""
        request_params_raw = {}
        for param in supported_search_fields:
            if param in arguments:
                request_params_raw[param] = arguments[param]
        request_params = cls.sanitize_url_params(request_params_raw)
        return request_params

    @classmethod
    def sanitize_url_params(cls, params):
        """Sanitize URL arguments for the Halo API

        In most cases, the Halo API will only honor the last value
        in URL arguments when multiple arguments have the same key.
        For instance: Requests builds URL arguments from a list a little
        strangely:
        {key:[val1, val2]}
        becomes key=val1&key=val2
        and not key=val1,val2.  If we let a
        list type object slide through, only val2 will be evaluated, and
        val1 is ignored by the Halo API.

        Args:
            params (dict): Parameters to be sanitized.

        Returns:
            dict

        """
        params_working = params.copy()
        for key, value in params_working.items():
            if isinstance(value, list):
                value_corrected = ",".join(value)
                params[key] = value_corrected
            elif isinstance(value, datetime.datetime):
                value_corrected = cls.datetime_to_8601(value)
                params[key] = value_corrected
            elif value is True:
                params[key] = "true"
            elif value is False:
                params[key] = "false"
        return params

    @classmethod
    def policy_to_dict(cls, policy):
        """Ensure that policy is a dictionary object"""
        if isinstance(policy, dict):
            return policy
        else:
            return json.loads(policy)

    @classmethod
    def merge_dicts(cls, first, second):
        """Merges dictionaries"""
        final = first.copy()
        final.update(second)
        return final

    @classmethod
    def verify_pages(cls, max_pages):
        """Verify the user isn't trying to pull too many pages in one query"""
        valid = True
        fail_msg = None
        if not isinstance(max_pages, int):
            fail_msg = "Type wrong for max_pages.  Should be int."
            return(False, fail_msg)
        if max_pages > 300:
            fail_msg = "You're asking for too many pages.  300 max."
            return(False, fail_msg)
        return(valid, fail_msg)

    @classmethod
    def parse_status(cls, url, resp_code, resp_text):
        """Parse status from HTTP response"""
        success = True
        exc = None
        if resp_code not in [200, 201, 202, 204]:
            success = False
            bad_statuses = {400: CloudPassageValidation(resp_text, code=400),
                            401: CloudPassageAuthentication(resp_text,
                                                            code=401),
                            404: CloudPassageResourceExistence(resp_text,
                                                               code=404,
                                                               url=url),
                            403: CloudPassageAuthorization(resp_text,
                                                           code=403),
                            422: CloudPassageValidation(resp_text, code=422),
                            429: CloudPassageRateLimit(resp_text, code=429)}
            if resp_code in bad_statuses:
                return(success, bad_statuses[resp_code])
            else:
                return(success, CloudPassageGeneral(resp_text, code=resp_code))
        return success, exc

    @classmethod
    def time_string_now(cls):
        """Returns an ISO 8601 formatted string for now, in UTC

        Returns:
            str: ISO 8601 formatted string

        """

        now = datetime.datetime.utcnow()
        return cls.datetime_to_8601(now)

    @classmethod
    def datetime_to_8601(cls, original_time):
        """Converts a datetime object to ISO 8601 formatted string.

        Args:
            dt (datetime.datetime): Datetime-type object

        Returns:
            str: ISO 8601 formatted string

        """
        time_split = (original_time.year, original_time.month,
                      original_time.day, original_time.hour,
                      original_time.minute, original_time.second,
                      original_time.microsecond)
        return "%04d-%02d-%02dT%02d:%02d:%02d.%06dZ" % time_split

    @classmethod
    def verify_python_version(cls, act_version, target_version):
        """Verifies that the installed version of Python meets requirements

        Args:
            str: Actual version, represented as a dotted string "2.4.9"
            dict: Target minimum versions, Keys are major versions.
                Values are represented as a dotted string "2.7.10"

        Returns:
            bool: True if it meets or exceeds the target minimum version.
        """
        maj_ver = act_version[0]
        try:
            if (LooseVersion(act_version) <
                    LooseVersion(target_version[maj_ver])):
                return False
            else:
                return True
        except KeyError:
            return False

    @classmethod
    def get_installed_python_version(cls):
        """Returns the current version of Python as a dotted string"""
        major, minor, micro = (sys.version_info.major, sys.version_info.minor,
                               sys.version_info.micro)
        installed_python_version = "{maj}.{min}.{mic}".format(maj=major,
                                                              min=minor,
                                                              mic=micro)
        return installed_python_version

    @classmethod
    def get_sdk_version(cls):
        """ Gets the version of the SDK """
        thisdir = os.path.dirname(__file__)
        initfile = os.path.join(thisdir, "__init__.py")
        with open(initfile, 'r') as i_file:
            raw_init_file = i_file.read()
        rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
        ver = rx_compiled.search(raw_init_file).group(1)
        return ver
