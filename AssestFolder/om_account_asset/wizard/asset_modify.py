# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree

from odoo import api, fields, models, _
# from odoo.osv.orm import setup_modifiers
class AssetAddInMaintenance(models.TransientModel):
    _name = 'asset.add.maintenance'
    _description = 'Add Asset'

    asset_id = fields.Many2one('account.asset.asset', string='Add Asset', required=True)

    def add_asset_method(self):
        """ Modifies the duration of asset for calculating depreciation
        and maintains the history of old values, in the chatter.
        """
        print(self.asset_id.id,'asset_idasset_idasset_idasset_idasset_id')
        list_ = {}
        if self.asset_id.id:
            print()
            acc_asset_id = self.env['account.asset.asset'].search([('id', '=',self.asset_id.id,)])
            # admin_asset_id = self.env['admin.assets'].search([('finance_asset_id', '=', vals['asset_id'])])
            # print(admin_asset_id, 'ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo')
            if acc_asset_id:
                name = acc_asset_id['name']
                id = acc_asset_id['id']
                print( acc_asset_id['manufacturer_id'],'ooooooooooqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
                print( acc_asset_id['partner_id'].id,'sssssssssssssssssssssssssssssssss')
                admin_asset_id = self.env['admin.assets'].search([('finance_asset_id', '=', id)])
                admin_id = admin_asset_id['id']
                currency_id = acc_asset_id['currency_id']
                company_id = acc_asset_id['company_id']
                category_id = acc_asset_id['category_id']

                manufacturer_id = acc_asset_id['manufacturer_id'].id
                print(manufacturer_id,'manufacturer_id===============================================================')
                start_date = acc_asset_id['start_date']
                warranty_start_date = acc_asset_id['warranty_start_date']
                warranty_end_date = acc_asset_id['warranty_end_date']
                purchase_date = acc_asset_id['purchase_date']
                vendor_id = acc_asset_id['partner_id'].id
                # criticality = acc_asset_id['criticality']
                date = acc_asset_id['date']
                # partner_id = acc_asset_id['partner_id']
                active = acc_asset_id['active']
                asset_number = acc_asset_id['asset_number']
                serial = acc_asset_id['serial']
                model = acc_asset_id['model']
                asset_maintenance_create = self.env['asset.asset'].create({
                    'name': name,
                    'finances_asset_id': id,
                    'admin_asset_id': admin_id,
                    'manufacturer_id':manufacturer_id,
                    'warranty_start_date':warranty_start_date,
                    'warranty_end_date':warranty_end_date,
                    'purchase_date':purchase_date,
                    'start_date':start_date,
                    'vendor_id':vendor_id,
                    'criticality': '',
                    # 'user_id':'',
                    'active': active,
                    'asset_number': asset_number,
                    'model': model,
                    'serial': serial,
                    # 'vendor_id': partner_id.id,
                    # 'purchase_date': date,
                })
                admin_asset_id = self.env['admin.assets'].search([('finance_asset_id', '=', id)])
                if admin_asset_id:
                    asset_maintenance_create.write({
                        'property_stock_asset': admin_asset_id['property_stock_asset'],
                        'user_id': admin_asset_id['user_id']
                    })
                    acc_asset_id.write({
                        'maintanance_asset': True
                    })
                else:
                    acc_asset_id.write({
                        'maintanance_asset': True
                    })
        return {'type': 'ir.actions.act_window_close'}



class AssetModify(models.TransientModel):
    _name = 'asset.modify'
    _description = 'Modify Asset'

    name = fields.Text(string='Reason', required=True)
    method_number = fields.Integer(string='Number of Depreciations', required=True)
    method_period = fields.Integer(string='Period Length')
    method_end = fields.Date(string='Ending date')
    asset_method_time = fields.Char(compute='_get_asset_method_time', string='Asset Method Time', readonly=True)


    def _get_asset_method_time(self):
        if self.env.context.get('active_id'):
            asset = self.env['account.asset.asset'].browse(self.env.context.get('active_id'))
            self.asset_method_time = asset.method_time

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     result = super(AssetModify, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
    #     asset_id = self.env.context.get('active_id')
    #     active_model = self.env.context.get('active_model')
    #     if active_model == 'account.asset.asset' and asset_id:
    #         asset = self.env['account.asset.asset'].browse(asset_id)
    #         doc = etree.XML(result['arch'])
    #         if asset.method_time == 'number' and doc.xpath("//field[@name='method_end']"):
    #             node = doc.xpath("//field[@name='method_end']")[0]
    #             node.set('invisible', '1')
    #             setup_modifiers(node, result['fields']['method_end'])
    #         elif asset.method_time == 'end' and doc.xpath("//field[@name='method_number']"):
    #             node = doc.xpath("//field[@name='method_number']")[0]
    #             node.set('invisible', '1')
    #             setup_modifiers(node, result['fields']['method_number'])
    #         result['arch'] = etree.tostring(doc, encoding='unicode')
    #     return result

    @api.model
    def default_get(self, fields):
        res = super(AssetModify, self).default_get(fields)
        asset_id = self.env.context.get('active_id')
        asset = self.env['account.asset.asset'].browse(asset_id)
        if 'name' in fields:
            res.update({'name': asset.name})
        if 'method_number' in fields and asset.method_time == 'number':
            res.update({'method_number': asset.method_number})
        if 'method_period' in fields:
            res.update({'method_period': asset.method_period})
        if 'method_end' in fields and asset.method_time == 'end':
            res.update({'method_end': asset.method_end})
        if self.env.context.get('active_id'):
            active_asset = self.env['account.asset.asset'].browse(self.env.context.get('active_id'))
            res['asset_method_time'] = active_asset.method_time
        return res

    
    def modify(self):
        """ Modifies the duration of asset for calculating depreciation
        and maintains the history of old values, in the chatter.
        """
        asset_id = self.env.context.get('active_id', False)
        asset = self.env['account.asset.asset'].browse(asset_id)
        old_values = {
            'method_number': asset.method_number,
            'method_period': asset.method_period,
            'method_end': asset.method_end,
        }
        asset_vals = {
            'method_number': self.method_number,
            'method_period': self.method_period,
            'method_end': self.method_end,
        }
        asset.write(asset_vals)
        asset.compute_depreciation_board()
        tracked_fields = self.env['account.asset.asset'].fields_get(['method_number', 'method_period', 'method_end'])
        changes, tracking_value_ids = asset._message_track(tracked_fields, old_values)
        if changes:
            asset.message_post(subject=_('Depreciation board modified'), body=self.name, tracking_value_ids=tracking_value_ids)
        return {'type': 'ir.actions.act_window_close'}
