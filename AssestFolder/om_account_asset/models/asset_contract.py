from odoo import api, fields, models,tools, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class AssetLogFuel(models.Model):
    _name ='asset.log.fuel.cost'
    _rec_name = 'asset_id'
    # _description = 'Fuel log for Asset'

    # @api.model
    # def default_get(self, default_fields):
    #     res = super(FleetVehicleLogFuel, self).default_get(default_fields)
    #     service = self.env.ref('fleet.type_service_refueling', raise_if_not_found=False)
    #     res.update({
    #         'date': fields.Date.context_today(self),
    #         'cost_subtype_id': service and service.id or False,
    #         'cost_type': 'fuel'
    #     })
    #     return res

    liter = fields.Float()
    price_per_liter = fields.Float()
    purchaser_id = fields.Many2one('res.partner', string='Purchaser')
    inv_ref = fields.Char('Invoice Reference', size=64)
    asset_id = fields.Many2one('account.asset.asset', string='Asset', required=True, ondelete='cascade')
    vendor_id = fields.Many2one('res.partner', 'Vendor')
    notes = fields.Text()
    date = fields.Date(string='Date', track_visibility="onchange")
    # we need to keep this field as a related with store=True because the graph view doesn't support
    # (1) to address fields from inherited table
    # (2) fields that aren't stored in database
    # cost_amount = fields.Float(related='cost_id.amount', string='Amount', store=True, readonly=False)
    amount = fields.Float(string='Amount', store=True, readonly=False)
    # odometer = fields.Float(compute="_get_odometer", inverse='_set_odometer', string='Odometer Value',
    #     help='Odometer measure of the vehicle at the moment of this log')
    odometer = fields.Float(string='Odometer Value',
        help='Odometer measure of the vehicle at the moment of this log')
    odometer_unit = fields.Selection([
        ('kilometers', 'Kilometers'),
        ('miles', 'Miles')
    ], 'Odometer Unit', default='kilometers', help='Unit of the odometer ', required=True)

    @api.onchange('asset_id')
    def _onchange_asset(self):
        if self.asset_id:
            self.vendor_id = self.asset_id.partner_id

    # def _get_odometer(self):
    #     self.odometer = 0.0
    #     for record in self:
    #         record.odometer = False
    #         if record.odometer_id:
    #             record.odometer = record.odometer_id.value
    #
    # def _set_odometer(self):
    #     for record in self:
    #         if not record.odometer:
    #             raise UserError(_('Emptying the odometer value of a vehicle is not allowed.'))
    #         odometer = self.env['fleet.vehicle.odometer'].create({
    #             'value': record.odometer,
    #             'date': record.date or fields.Date.context_today(record),
    #             'vehicle_id': record.vehicle_id.id
    #         })
    #         self.odometer_id = odometer


    # @api.onchange('vehicle_id')
    # def _onchange_vehicle(self):
    #     if self.vehicle_id:
    #         self.odometer_unit = self.vehicle_id.odometer_unit
    #         self.purchaser_id = self.vehicle_id.driver_id.id
    #
    # @api.onchange('liter', 'price_per_liter', 'amount')
    # def _onchange_liter_price_amount(self):
    #     # need to cast in float because the value receveid from web client maybe an integer (Javascript and JSON do not
    #     # make any difference between 3.0 and 3). This cause a problem if you encode, for example, 2 liters at 1.5 per
    #     # liter => total is computed as 3.0, then trigger an onchange that recomputes price_per_liter as 3/2=1 (instead
    #     # of 3.0/2=1.5)
    #     # If there is no change in the result, we return an empty dict to prevent an infinite loop due to the 3 intertwine
    #     # onchange. And in order to verify that there is no change in the result, we have to limit the precision of the
    #     # computation to 2 decimal
    #     liter = float(self.liter)
    #     price_per_liter = float(self.price_per_liter)
    #     amount = float(self.amount)
    #     if liter > 0 and price_per_liter > 0 and round(liter * price_per_liter, 2) != amount:
    #         self.amount = round(liter * price_per_liter, 2)
    #     elif amount > 0 and liter > 0 and round(amount / liter, 2) != price_per_liter:
    #         self.price_per_liter = round(amount / liter, 2)
    #     elif amount > 0 and price_per_liter > 0 and round(amount / price_per_liter, 2) != liter:
    #         self.liter = round(amount / price_per_liter, 2)

class AssetServiceType(models.Model):
    _name = 'asset.service.type'
    _description = 'Asset Service Type'
    _rec_name = 'service_description'

    service_description = fields.Text()
    amount = fields.Float(string='Amount', store=True, readonly=False)
    contract_id = fields.Many2one('contract.asset', string='Contract', required=True, ondelete='cascade')
    asset_id = fields.Many2one('account.asset.asset', string='Asset', required=True, ondelete='cascade')



class AssetContract(models.Model):
    _name = 'contract.asset'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Contract information on a Asset'
    ins_ref = fields.Char('Contract Reference', size=64, copy=False)
    asset_id = fields.Many2one('account.asset.asset', string='Asset', required=True, ondelete='cascade')
    included_services = fields.One2many('asset.service.type', 'contract_id', required=False, ondelete='cascade')
    type = fields.Selection([
        ('Lease', 'Lease'),
        ('Contract', 'Contract'),
        ('Service', 'Service'),
        ('AMC', 'AMC')
        ],  required=True)
    activation_amount = fields.Float(string='Activation Cost', store=True, readonly=False)
    insurer_id = fields.Many2one('res.partner', 'Vendor')
    user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user, index=True)
    purchaser_id = fields.Many2one('res.partner',string= 'Asset Assigned To', default=lambda self: self.env.user.partner_id.id,
        help='Person to which the contract is signed for')
    odometer = fields.Float(string='Creation Contract Odometer',
        help='Odometer measure of the vehicle at the moment of the contract creation')

    date = fields.Date(string='Invoice Date', track_visibility="onchange")
    start_date = fields.Date('Contract Start Date', default=fields.Date.context_today,
                             help='Date when the coverage of the contract begins')
    expiration_date = fields.Date(string='Contract Expiration Date',required=True,
                                  help='Date when the coverage of the contract expirates (by default, one year after begin date)')
    notes = fields.Text('Terms and Conditions', help='Write here all supplementary information relative to this contract', copy=False)



    name = fields.Text(compute='_compute_contract_name', store=True)

    active = fields.Boolean(default=True)


    days_left = fields.Integer(compute='_compute_days_left', string='Warning Date')


    state = fields.Selection([
        ('futur', 'Incoming'),
        ('open', 'In Progress'),
        ('diesoon', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('closed', 'Closed')
        ], 'Status', default='open', readonly=True,
        help='Choose whether the contract is still valid or not',
        tracking=True,
        copy=False)
    cost_generated = fields.Float('Recurring Cost Amount', tracking=True,
        help="Costs paid at regular intervals, depending on the cost frequency. "
        "If the cost frequency is set to unique, the cost will be logged at the start date")
    cost_frequency = fields.Selection([
        ('no', 'No'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
        ], 'Recurring Cost Frequency', default='no', help='Frequency of the recuring cost', required=True)
    sum_cost = fields.Float(compute='_compute_sum_cost', string='Indicative Costs Total')
    # we need to keep this field as a related with store=True because the graph view doesn't support
    # (1) to address fields from inherited table
    # (2) fields that aren't stored in database
    # cost_amount = fields.Float(related='cost_id.amount', string='Amount', store=True, readonly=False)

    @api.model
    def create(self, vals):
        asset = super(AssetContract, self.with_context(mail_create_nolog=True)).create(vals)
        try:
            if vals['included_services']:
                self.env['asset.service.type'].create({
                    'contract_id': asset.id,
                    'service_description': vals['included_services'][0][2]['service_description'],
                    'amount': vals['included_services'][0][2]['amount'],
                    'asset_id': asset.asset_id.id,
                })
                return asset
        except:
            return asset

    @api.onchange('asset_id')
    def _onchange_asset(self):
        if self.asset_id:
            self.purchaser_id = self.asset_id.partner_id
            # self.asset_id = self.generated_cost_ids.asset_id

    def contract_close(self):
        for record in self:
            record.state = 'closed'

    def contract_open(self):
        for record in self:
            record.state = 'open'

    def act_renew_contract(self):
        assert len(self.ids) == 1, "This operation should only be done for 1 single contract at a time, as it it suppose to open a window as result"
        for element in self:
            # compute end date
            print(element.asset_id.id,'ppppppppppppppppppppppppppppppppppppppppppppppp33333333333333333333333333333333')
            startdate = fields.Date.from_string(element.start_date)
            enddate = fields.Date.from_string(element.expiration_date)
            diffdate = (enddate - startdate)
            default = {
                'date': fields.Date.context_today(self),
                'start_date': fields.Date.to_string(fields.Date.from_string(element.expiration_date) + relativedelta(days=1)),
                'expiration_date': fields.Date.to_string(enddate + diffdate),
            }
            newid = element.copy(default).id
            id=self.id
            self.env.cr.execute(
                f"""SELECT asset_id, service_description, amount
FROM public.asset_service_type where contract_id= {id}""")
            record = self.env.cr.fetchall()
            print(record,'ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp')
            services = self.env['asset.service.type'].create({
                    'contract_id':newid,
                    'service_description': record[0][1],
                    'amount': record[0][2],
                    'asset_id': element.asset_id.id,
                })
        return {
            'name': _("Renew Contract"),
            'view_mode': 'form',
            'view_id': self.env.ref('om_account_asset.asset_contract_view_form').id,
            'res_model': 'contract.asset',
            'type': 'ir.actions.act_window',
            'domain': '[]',
            'res_id': newid,
            'context': {'active_id': newid},
        }

    @api.depends('expiration_date', 'state')
    def _compute_days_left(self):
        """return a dict with as value for each contract an integer
        if contract is in an open state and is overdue, return 0
        if contract is in a closed state, return -1
        otherwise return the number of days before the contract expires
        """
        for record in self:
            if record.expiration_date and record.state in ['open', 'diesoon', 'expired']:
                today = fields.Date.from_string(fields.Date.today())
                renew_date = fields.Date.from_string(record.expiration_date)
                diff_time = (renew_date - today).days
                record.days_left = diff_time > 0 and diff_time or 0
            else:
                record.days_left = -1
