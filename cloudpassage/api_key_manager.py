"""CloudPassage Api Key Manager"""

import os
import yaml
import cloudpassage.sanity as sanity


class ApiKeyManager(object):
    """Retrieves API keys from file or environment.

    If instantiated with no arguments, it will return credentials from
    environment variables.  If there are no credentials set in environment
    variables, it will look to /etc/cloudpassage.yaml.

    If there is no api_hostname specified in the selected configuration
    source, it defaults to api.cloudpassage.com.


    Environment variables::
        HALO_API_KEY

        HALO_API_SECRET_KEY

        HALO_API_HOSTNAME

        HALO_API_PORT


    Yaml file structure::
        defaults:

            key_id:

            secret_key:

            api_hostname:

            api_port:


    Keyword args:
        config_file (str): full path to yaml config file


    Attributes:
        api_hostname: Hostname of api endpoint. \
        Defaults to api.cloudpassage.com
        api_port: API port
        key_id: API key ID
        secret_key: API key secret

    """

    def __init__(self, **kwargs):
        self.api_hostname = "api.cloudpassage.com"
        self.key_id = None
        self.secret_key = None
        self.api_port = 443
        self.config_file = None

        if "config_file" in kwargs:
            self.config_file = kwargs["config_file"]
        else:
            self.config_file = "/etc/cloudpassage.yaml"
        env_config = self.get_config_from_env()
        file_config = self.get_config_from_file(self.config_file)
        if env_config is not None:
            self.set_config_variables(env_config)
            return
        if file_config is not None:
            self.set_config_variables(file_config)
        return

    def set_config_variables(self, config_variables):
        """Sets configuration vars for object"""
        self.key_id = config_variables["key_id"]
        self.secret_key = config_variables["secret_key"]
        if sanity.validate_api_hostname(config_variables["api_hostname"]):
            self.api_hostname = config_variables["api_hostname"]
        try:
            if 65535 > int(config_variables["api_port"]) > 0:
                self.api_port = int(config_variables["api_port"])
        except:
            self.api_port = 443
        return

    def get_config_from_file(self, config_file):
        """Extracts config from file"""
        session_yaml = None
        try:
            with open(self.config_file) as y_config_file:
                session_yaml = yaml.load(y_config_file)["defaults"]
        except IOError:
            error_message = "Unable to load config from file: %s" % config_file
            print error_message
        return session_yaml

    def get_config_from_env(self):
        """Derives config information from environment vars"""
        config = None
        env_variables = {"key_id": os.getenv("HALO_API_KEY"),
                         "secret_key": os.getenv("HALO_API_SECRET_KEY"),
                         "api_hostname": os.getenv("HALO_API_HOSTNAME"),
                         "api_port": os.getenv("HALO_API_PORT")}
        if self.env_vars_are_set(env_variables):
            config = env_variables
        return config

    @classmethod
    def env_vars_are_set(cls, env_vars):
        """Determine if environment vars are correctly set"""
        vars_are_set = True
        if env_vars["key_id"] is None or env_vars["secret_key"] is None:
            vars_are_set = False
        return vars_are_set
