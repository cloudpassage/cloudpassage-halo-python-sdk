"""CloudPassage init"""
from cloudpassage.agent_upgrade import AgentUpgrade  # noqa: F401
from cloudpassage.alert_profile import AlertProfile  # noqa: F401
from cloudpassage.api_key_manager import ApiKeyManager  # noqa: F401
from cloudpassage.configuration_policy import ConfigurationPolicy  # noqa: F401
from cloudpassage.cve_exception import CveException  # noqa: F401
from cloudpassage.cve_exception import CveExceptions  # noqa: F401
from cloudpassage.cve_details import CveDetails  # noqa: F401
from cloudpassage.fim_policy import FimPolicy  # noqa: F401
from cloudpassage.fim_policy import FimBaseline  # noqa: F401
from cloudpassage.event import Event  # noqa: F401
from cloudpassage.exceptions import CloudPassageAuthentication  # noqa: F401
from cloudpassage.exceptions import CloudPassageAuthorization  # noqa: F401
from cloudpassage.exceptions import CloudPassageCollision  # noqa: F401
from cloudpassage.exceptions import CloudPassageGeneral  # noqa: F401
from cloudpassage.exceptions import CloudPassageInternalError  # noqa: F401
from cloudpassage.exceptions import CloudPassageResourceExistence  # noqa: F401
from cloudpassage.exceptions import CloudPassageValidation  # noqa: F401
from cloudpassage.exceptions import CloudPassageRateLimit  # noqa: F401
from cloudpassage.firewall_policy import FirewallInterface  # noqa: F401
from cloudpassage.firewall_policy import FirewallPolicy  # noqa: F401
from cloudpassage.firewall_policy import FirewallRule  # noqa: F401
from cloudpassage.firewall_policy import FirewallService  # noqa: F401
from cloudpassage.firewall_policy import FirewallZone  # noqa: F401
from cloudpassage.halo import HaloSession  # noqa: F401
from cloudpassage.http_helper import HttpHelper  # noqa: F401
from cloudpassage.issue import Issue  # noqa: F401
from cloudpassage.lids_policy import LidsPolicy  # noqa: F401
from cloudpassage.local_user_account import LocalUserAccount  # noqa: F401
from cloudpassage.local_user_group import LocalUserGroup  # noqa: F401
from cloudpassage.scan import Scan  # noqa: F401
from cloudpassage.server import Server  # noqa: F401
from cloudpassage.server_group import ServerGroup  # noqa: F401
from cloudpassage.special_events_policy import SpecialEventsPolicy  # NOQA
from cloudpassage.system_announcement import SystemAnnouncement  # noqa: F401
from cloudpassage.time_series import TimeSeries  # noqa: F401
from cloudpassage.utility import Utility as init_util
from cloudpassage.csp_accounts import CspAccount  # noqa: F401
from cloudpassage.csp_findings import CspFinding  # noqa: F401
from cloudpassage.csp_resources import CspResource  # noqa: F401
from cloudpassage.csp_scanner_settings import CspSetting  # noqa: F401
from cloudpassage.container import Container  # noqa: F401
from cloudpassage.container_event import ContainerEvent  # noqa: F401
from cloudpassage.container_image import ContainerImage  # noqa: F401
from cloudpassage.container_package import ContainerPackage  # noqa: F401
from cloudpassage.container_process import ContainerProcess  # noqa: F401
from cloudpassage.image_issue import ImageIssue  # noqa: F401
from cloudpassage.image_registry import ImageRegistry  # noqa: F401
from cloudpassage.image_repo import ImageRepo  # noqa: F401


minimum = {"2": "2.7.10", "3": "3.6.5"}
installed = init_util.get_installed_python_version()
if init_util.verify_python_version(installed, minimum) is False:
    err_msg = "Warning: Minimum supported Python version %s" % minimum
    print(err_msg)

__author__ = "CloudPassage"
__version__ = "1.6.5"
__license__ = "BSD"
