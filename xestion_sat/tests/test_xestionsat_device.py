# 1: imports of python lib
from datetime import datetime

# 2: import of known third party lib

# 3:  imports of odoo
from .test_common import TestCommonData
from odoo.exceptions import ValidationError

# 4:  imports from odoo modules

# 5: local imports

# 6: Import of unknown third party lib


class XestionsatTestDevice(TestCommonData):
    """Test.
    """

    def setUp(self):
        super(XestionsatTestDevice, self).setUp()
        self.Device = self.env['xestionsat.device']

    def test_create_device(self):
        """Test.
        """

        # Device 1
        self.device_1 = self.Device.sudo(self.test_admin_1).create(
            {
                # Required fields
                'created_by_id': self.test_admin_1.id,
                'owner_id': self.partner_1.id,
                'headquarter_id': self.partner_1_address_2.id,
                'name': 'Equipo 1',
                'state': 'operational',

                # Optional fields
                'user_ids': [
                    self.partner_1_employee_1,
                    self.partner_1_employee_2,
                ],
                'devicecomponents_ids': [
                    self.product_1,
                    self.product_2,
                ],
                'internal_id': '20-000001',
                'location': 'Sala de reunións grande',
                'description': 'Equipo para presentacións',
                'observation': 'Saídas de video: 2xHDMI, 1xDVI e 1xVGA',
                'date_registration': datetime.now().strftime('%Y-%m-%d'),
                # 'date_cancellation': '',
            }
        )

        # Check that device is created or not
        assert self.device_1, "Device not created"

        # Check Odoo user constraint
        with self.assertRaises(ValidationError):
            self.device_1.created_by_id = self.test_admin_2

        # Check headquarters constraints
        with self.assertRaises(ValidationError):
            self.device_1.headquarter_id = self.partner_2_address_2

        # Check device user constraint
        with self.assertRaises(ValidationError):
            self.device_1.user_ids.append(self.partner_2_employee_2)
