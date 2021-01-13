
import sys
import logging

from shellfoundry.releasetools.test_helper import create_autoload_context_2g

from src.driver import IxChariotServer2GDriver

client_install_path = 'E:/Program Files (x86)/Ixia/IxChariot/webapi-96'
address = '192.168.42.167'
user = 'admin'
password = 'DxTbqlSgAVPmrDLlHvJrsA=='


class TestIxChariotServer2GDriver():

    def setup(self):
        self.context = create_autoload_context_2g(model='IxChariot Server Shell 2G', address=address,
                                                  user=user, password=password,
                                                  client_install_path=client_install_path)
        self.driver = IxChariotServer2GDriver()
        self.driver.initialize(self.context)
        self.driver.logger.addHandler(logging.StreamHandler(sys.stdout))

    def teardown(self):
        pass

    def test_autoload(self):
        inventory = self.driver.get_inventory(self.context)
        print('\n')
        for r in inventory.resources:
            print('{}, {}, {}'.format(r.relative_address, r.model, r.name))
        print('\n')
        for a in inventory.attributes:
            print('{}, {}, {}'.format(a.relative_address, a.attribute_name, a.attribute_value))
