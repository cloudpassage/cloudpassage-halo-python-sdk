"""CveDetail Class"""

import cloudpassage.sanity as sanity
import cloudpassage.utility as utility
from cloudpassage.http_helper import HttpHelper


class CveDetails(object):
    """Initializing the CveDetail class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    def __init__(self, session):
        self.session = session
        return None

    def describe(self, cve_id):
        """Describe a CVE with complete information on one Common
           Vulnerability and Exposure (CVE), as defined by the National
           Institute of Standards and Technology (NIST).

        Args:
            cve_id (str): CVE number

        Returns:
            dict: Dictionary object describing the details of the
                  Common Vulnerability and Exposure specified by CVE number.

        """

        endpoint = "/v1/cve_details/%s" % cve_id
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        return response