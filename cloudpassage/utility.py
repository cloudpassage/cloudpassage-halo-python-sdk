"""General utilities"""


import json
import datetime
import os
import re
import sys
from cloudpassage.exceptions import CloudPassageValidation
from cloudpassage.exceptions import CloudPassageAuthentication
from cloudpassage.exceptions import CloudPassageAuthorization
from cloudpassage.exceptions import CloudPassageResourceExistence
from cloudpassage.exceptions import CloudPassageGeneral
from cloudpassage.exceptions import CloudPassageRateLimit
from distutils.version import LooseVersion


def determine_policy_metadata(policy):
    """Accepts string or dict.  Returns dict of policy
    type, name, and target platform.

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

    """

    working_pol = None
    return_body = {"policy_type": None,
                   "policy_name": None,
                   "target_platform": None}
    # if type(policy) is str:
    if isinstance(policy, str):
        working_pol = json.loads(policy)
    elif isinstance(policy, dict):
        working_pol = policy.copy()
    else:
        print "Policy type must be str or dict!"
    try:
        derived_type = working_pol.items()[0][0]
        if derived_type == "fim_policy":
            return_body["policy_type"] = "FIM"
        if derived_type == "policy":
            return_body["policy_type"] = "CSM"
        if derived_type == "lids_policy":
            return_body["policy_type"] = "LIDS"
        if derived_type == "firewall_policy":
            return_body["policy_type"] = "Firewall"
    except AttributeError:
        pass
    try:
        return_body["policy_name"] = working_pol.items()[0][1]["name"]
    except AttributeError:
        pass
    try:
        derived_platform = working_pol.items()[0][1]["platform"]
        if derived_platform == 'linux':
            return_body["target_platform"] = 'Linux'
        elif derived_platform == 'windows':
            return_body["target_platform"] = 'Windows'
    except AttributeError:
        pass
    return return_body


def assemble_search_criteria(supported_search_fields, arguments):
    """Verifies request params and returns a dict of validated arguments"""
    request_params_raw = {}
    for param in supported_search_fields:
        if param in arguments:
            request_params_raw[param] = arguments[param]
    request_params = sanitize_url_params(request_params_raw)
    return request_params


def sanitize_url_params(params):
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

    """
    params_working = params.copy()
    for key, value in params_working.items():
        if isinstance(value, list):
            value_corrected = ",".join(value)
            params[key] = value_corrected
        if isinstance(value, datetime.datetime):
            value_corrected = datetime_to_8601(value)
            params[key] = value_corrected
    return params


def policy_to_dict(policy):
    """Ensures that policy is a dictionary object"""
    if isinstance(policy, dict):
        return policy
    else:
        return json.loads(policy)


def merge_dicts(first, second):
    """Merges dictionaries"""
    final = first.copy()
    final.update(second)
    return final


def verify_pages(max_pages):
    """Verify the user isn't trying to pull too many pages in one query"""
    valid = True
    fail_msg = None
    if not isinstance(max_pages, int):
        fail_msg = "Type wrong for max_pages.  Should be int."
        valid = False
    if max_pages > 300:
        fail_msg = "You're asking for too many pages.  300 max."
        valid = False
    return(valid, fail_msg)


def parse_status(url, resp_code, resp_text):
    """Parse status from HTTP response"""
    success = True
    exc = None
    if resp_code not in [200, 201, 202, 204]:
        success = False
        bad_statuses = {400: CloudPassageValidation(resp_text, code=400),
                        401: CloudPassageAuthentication(resp_text, code=401),
                        404: CloudPassageResourceExistence(resp_text, code=404,
                                                           url=url),
                        403: CloudPassageAuthorization(resp_text, code=403),
                        422: CloudPassageValidation(resp_text, code=422),
                        429: CloudPassageRateLimit(resp_text, code=429)}
        if resp_code in bad_statuses:
            return(success, bad_statuses[resp_code])
        else:
            return(success, CloudPassageGeneral(resp_text, code=resp_code))
    return success, exc


def time_string_now():
    """Returns an ISO 8601 formatted string for now, in UTC

    Returns:
        str: ISO 8601 formatted string

    """

    now = datetime.datetime.utcnow()
    return datetime_to_8601(now)


# There should be a built-in function for coverting to 8601.
def datetime_to_8601(original_time):
    """Converts a datetime object to ISO 8601 formatted string.

    Args:
        dt (datetime.datetime): Datetime-type object

    Returns:
        str: ISO 8610 formatted string

    """

    time_split = (original_time.year, original_time.month, original_time.day,
                  original_time.hour, original_time.minute,
                  original_time.second, original_time.microsecond)
    return "%04d-%02d-%02dT%02d:%02d:%02d.%06dZ" % time_split


def verify_python_version(actual_version, target_version):
    """Verifies that the installed version of Python meets minimum requirements

    Args:
        str: Actual version, represented as a dotted string "2.4.9"
        str: Target minimum version, represented as a dotted string "2.7.10"

    Returns:
        bool: True if it meets or exceeds the target minimum version.
    """
    if LooseVersion(actual_version) < LooseVersion(target_version):
        return False
    else:
        return True


def get_installed_python_version():
    """Returns the version of Python currently running as a dotted string"""
    installed_python_version = "%s.%s.%s" % (str(sys.version_info.major),
                                             str(sys.version_info.minor),
                                             str(sys.version_info.micro))
    return installed_python_version


def get_sdk_version():
    """ Gets the version of the SDK """
    thisdir = os.path.dirname(__file__)
    initfile = os.path.join(thisdir, "__init__.py")
    with open(initfile, 'r') as i_file:
        raw_init_file = i_file.read()
    rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
    ver = rx_compiled.search(raw_init_file).group(1)
    return ver
