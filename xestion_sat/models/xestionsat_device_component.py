# 1: imports of python lib
from lxml import etree

# 2: import of known third party lib

# 3:  imports of odoo
from odoo import models, fields, api, _

# 4:  imports from odoo modules
from .xestionsat_common import NEW_COMPONENT
from .xestionsat_message import MESSAGE

# 5: local imports

# 6: Import of unknown third party lib


class DeviceComponent(models.Model):
    """Model to describe the components that make up each device.
    """
    ###########################################################################
    # Private attributes
    ###########################################################################
    _name = 'xestionsat.device.component'
    _description = _('Device - Component')
    _inherits = {'product.product': 'product_id'}
    _inherit = ['mail.thread']

    ###########################################################################
    # Fields declaration
    ###########################################################################
    # -------------------------------------------------------------------------
    # Relational Fields
    # -------------------------------------------------------------------------
    product_id = fields.Many2one(
        'product.product',
        string='Compponent',
        ondelete='restrict',
        required=True,
    )
    device_id = fields.Many2one(
        'xestionsat.device',
        string='ID device',
        ondelete='restrict',
    )

    # -------------------------------------------------------------------------
    # Other Fields
    # -------------------------------------------------------------------------
    serial = fields.Char(
        string='Serial number',
    )
    observation = fields.Text(
        string='Observations',
    )

    date_registration = fields.Datetime(
        string='Registration date',
        default=lambda *a: fields.Datetime.now(),
        required=True,
    )
    date_cancellation = fields.Datetime(
        string='Date of cancellation',
    )

    ###########################################################################
    # Constraints and onchanges
    ###########################################################################
    @api.constrains('date_registration', 'date_cancellation')
    def _check_date_end(self):
        """Check that the cancellation date is not earlier than the start registration.
        """
        for record in self:
            if record.date_cancellation:
                if record.date_cancellation < record.date_registration:
                    raise models.ValidationError(
                        _(MESSAGE['component_constraint']['date_cancellation'])
                    )

    ###########################################################################
    # CRUD methods
    ###########################################################################
    @api.multi
    def create_new_component(
        self, name=NEW_COMPONENT, context=None, flags=None
    ):
        """Method to create a new add component according to the past context.

        :param name: View title.
        :param context: Context to present the view data.
        :param flags: Flags to modify the view.
        """
        if type(name) != str:
            name = NEW_COMPONENT

        return {
            'name': _(name),
            'type': 'ir.actions.act_window',
            'res_model': 'xestionsat.device.component',
            'view_type': 'form',
            'view_mode': 'form',
            'context': context,
            'target': 'new',
            'flags': flags,
        }

    ###########################################################################
    # Business methods
    ###########################################################################
    @api.model
    def fields_view_get(self, view_id=None, view_type=None, **kwargs):
        """Modify the resulting view according to user preferences.
        """
        context = self.env.context

        result = super(DeviceComponent, self).fields_view_get(
            view_id=view_id, view_type=view_type, **kwargs
        )

        doc = etree.XML(result['arch'])

        if view_type == 'form':
            if 'device_view' in context:
                # btn_close
                for node in doc.xpath("//button[@name='btn_close']"):
                    node.set('modifiers', '{}')

        result['arch'] = etree.tostring(doc)

        return result
