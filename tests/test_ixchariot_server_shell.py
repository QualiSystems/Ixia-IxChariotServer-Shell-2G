
"""
Tests for `IxiaChassisDriver`
"""

from cloudshell.api.cloudshell_api import ResourceAttributesUpdateRequest, AttributeNameValue, CloudShellAPISession

ixchariot_servers = {
    '96': {'address': '192.168.42.167',
           'client_install_path': 'E:/Program Files (x86)/Ixia/IxChariot/webapi-96',
           'user': 'admin',
           'password': 'admin',
           'eps': 1,
           }
    }


class TestIxiaChassis2GShell(object):

    session = None

    def setup(self):
        self.session = CloudShellAPISession('localhost', 'admin', 'admin', 'Global')

    def teardown(self):
        for resource in self.session.GetResourceList('Testing').Resources:
            self.session.DeleteResource(resource.Name)

    def test_hello_world(self):
        pass

    def test_all(self):
        for key, value in ixchariot_servers.items():
            self._get_inventory(key, value)

    def _get_inventory(self, name, properties):
        self.resource = self.session.CreateResource(resourceFamily='CS_TrafficGeneratorChassis',
                                                    resourceModel='IxChariot Server Shell 2G',
                                                    resourceName=name,
                                                    resourceAddress=properties['address'],
                                                    folderFullPath='Testing',
                                                    parentResourceFullPath='',
                                                    resourceDescription='should be removed after test')
        self.session.UpdateResourceDriver(self.resource.Name, 'IxChariot Server Shell 2G')
        attributes = [AttributeNameValue('IxChariot Server Shell 2G.Client Install Path',
                                         properties['client_install_path']),
                      AttributeNameValue('IxChariot Server Shell 2G.User', properties['user']),
                      AttributeNameValue('IxChariot Server Shell 2G.Password', properties['password'])]
        self.session.SetAttributesValues(ResourceAttributesUpdateRequest(self.resource.Name, attributes))
        self.session.AutoLoad(self.resource.Name)
        resource_details = self.session.GetResourceDetails(self.resource.Name)
        assert(len(resource_details.ChildResources) == properties['modules'])
        self.session.DeleteResource(self.resource.Name)
