"""Collection of functions for doing validation and sanity checking"""

import os
import re
from cloudpassage.exceptions import CloudPassageValidation


def validate_object_id(object_id):
    """Validates object ID (server_id, policy_id, etc...)

    This function validates Object IDs with the intent of guarding against \
    URL traversal.

    Args:
        object_id (str or list): Object ID to be validated

    Returns:
        (bool) True if valid, throws an exception otherwise.

    """

    rex = re.compile('^[A-Za-z0-9]+$')
    if isinstance(object_id, (str, unicode)):
        if not rex.match(object_id):
            error_message = "Object ID failed validation: %s" % object_id
            raise CloudPassageValidation(error_message)
        else:
            return True
    elif isinstance(object_id, list):
        for individual in object_id:
            if not rex.match(individual):
                error_message = "Object ID failed validation: %s" % object_id
                raise CloudPassageValidation(error_message)
        return True
    else:
        error_message = "Wrong type for object ID: %s" % str(type(object_id))
        raise TypeError(error_message)


def validate_api_hostname(api_hostname):
    """Validate hostname for API endpoint"""
    hostname_is_valid = False
    valid_api_host = re.compile(r'^([A-Za-z0-9-]+\.){1,2}cloudpassage\.com$')
    if valid_api_host.match(api_hostname):
        hostname_is_valid = True
    return hostname_is_valid


def validate_config_path(config_path):
    """Validate config file path exists"""
    if os.path.exists(config_path):
        return True


def validate_cve_exception_cbody(body):
    """Validate CVE Exception create request body"""
    if not set(("scope",
                "package_version",
                "package_name")) <= set(body):
        error_message = "scope, package_version and \
                         package_name are required fields."
        raise CloudPassageValidation(error_message)
    elif "server" in body.values() and "server_id" not in body.keys():
        error_message = "Required to provide server id for server scope."
        raise CloudPassageValidation(error_message)
    elif "group" in body.values() and "group_id" not in body.keys():
        error_message = "Required to provide group id for group scope."
        raise CloudPassageValidation(error_message)
    return True
