# -*- coding: utf-8 -*-

from odoo import models, fields, api

class accounting_cashflow(models.Model):
    _inherit = 'account.account'

    # _name = 'accounting_cashflow.accounting_cashflow'

    #
    # name = fields.Char()
    # value = fields.Integer()
    cashflow_type = fields.Selection([ ('operations', 'Operations'),('financing', 'Financing'),('investing','Investing')],'Cashflow Type')
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()
    #
    # @api.depends('value')
    # def _value_pc(self):
    #     self.value2 = float(self.value) / 100