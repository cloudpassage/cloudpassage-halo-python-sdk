"""CloudPassage init"""
from cloudpassage.agent_upgrade import AgentUpgrade  # noqa: F401
from cloudpassage.alert_profile import AlertProfile  # noqa: F401
from cloudpassage.api_key_manager import ApiKeyManager  # noqa: F401
from cloudpassage.configuration_policy import ConfigurationPolicy  # noqa: F401
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
from cloudpassage.retry import Retry  # noqa: F401
from cloudpassage.scan import CveException  # noqa: F401
from cloudpassage.scan import Scan  # noqa: F401
from cloudpassage.server import Server  # noqa: F401
from cloudpassage.server_group import ServerGroup  # noqa: F401
from cloudpassage.special_events_policy import SpecialEventsPolicy  # NOQA
from cloudpassage.system_announcement import SystemAnnouncement  # noqa: F401
from cloudpassage.time_series import TimeSeries  # noqa: F401
import utility as init_util


minimum = "2.7.10"
installed = init_util.get_installed_python_version()
if init_util.verify_python_version(installed, minimum) is False:
    err_msg = "Warning: Minimum supported Python version %s" % minimum
    print err_msg

__author__ = "CloudPassage"
__version__ = "1.1.3"
__license__ = "BSD"
