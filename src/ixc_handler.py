"""
IxChariot server (==chassis) shell driver implementation for Auto-load only.

@author: yoram-s@qualisystems.com
"""

import imp
import sys
import os

from cloudshell.shell.core.driver_context import AutoLoadDetails, AutoLoadResource, AutoLoadAttribute
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext


class IxcHandler(object):

    def initialize(self, context, logger):

        self.logger = logger

        address = context.resource.address
        username = context.resource.attributes['IxChariot Server Shell 2G.User']
        encripted_password = context.resource.attributes['IxChariot Server Shell 2G.Password']
        password = CloudShellSessionContext(context).get_api().DecryptPassword(encripted_password).Value
        client_install_path = context.resource.attributes['IxChariot Server Shell 2G.Client Install Path']

        sys.path.append(client_install_path)
        webapi = imp.load_source('webapi', os.path.join(client_install_path, 'ixia/webapi.py'))
        self.ixchariotapi = imp.load_source('ixchariotapi', os.path.join(client_install_path, 'ixchariotApi.py'))

        self.connection = webapi.webApi.connect('https://' + address, 'v1', None, username, password)

    def get_inventory(self, context):
        """ Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """

        self.attributes = []
        self.resources = []
        session = self.connection.createSession('ixchariot')
        session.startSession()
        self._get_server(session)

        return AutoLoadDetails(self.resources, self.attributes)

    def _get_server(self, session):
        """ Get server resource and attributes. """

        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='CS_TrafficGeneratorChassis.Model Name',
                                                 attribute_value='IxChariot Server'))

        endpoints = session.parentConvention.httpGet("ixchariot/resources/endpoint")
        for endpoint in endpoints:
            self.logger.info('endpoint = {}'.format(endpoint))
            self._get_endpoint(endpoint)

    def _get_endpoint(self, endpoint):
        """ Get endpoint resource and attributes. """

        relative_address = 'EP' + endpoint.name.encode('utf-8')
        model = 'IxChariot Server Shell 2G.GenericTrafficGeneratorModule'
        self.resources.append(AutoLoadResource(model=model,
                                               name=endpoint.name.encode('utf-8'),
                                               relative_address=relative_address))

        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name='CS_TrafficGeneratorModule.Model Name',
                                                 attribute_value='IxChariot Endpoint'))
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name=model + '.Management IP',
                                                 attribute_value=endpoint.managementIp.address))
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name=model + '.OS Version',
                                                 attribute_value=endpoint.operatingSystem))

        for test_ip in endpoint.ips:
            self.logger.info('test IP = {}'.format(test_ip))
            self._get_test_ip(relative_address, test_ip)

    def _get_test_ip(self, endpoint, test_ip):
        """ Get port group resource and attributes. """

        relative_address = endpoint + '/' + test_ip.address.encode('utf-8')
        model = 'IxChariot Server Shell 2G.GenericTrafficGeneratorPort'
        self.resources.append(AutoLoadResource(model=model,
                                               name=test_ip.address.encode('utf-8').replace(':', '-'),
                                               relative_address=relative_address))

        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name='CS_TrafficGeneratorPort.Model Name',
                                                 attribute_value='IxChariot Test IP'))
