# -*- coding: utf-8 -*-

from odoo import models, fields, api

class inventory_indosis(models.Model):
    _name = 'inventory_indosis.barang'

    name = fields.Char()
    qty = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    group_id = fields.Many2one('inventory_indosis.group', ondelete='set null', string="Group", index=True)
    image = fields.Binary()
    barcode = fields.Char()
    tipe_barang = fields.Char()

    # @api.depends('value')
    # def _value_pc(self):
    #     self.value2 = float(self.value) / 100

class Group(models.Model):
    _name = 'inventory_indosis.group'

    name = fields.Char(required=True)
    description = fields.Char()