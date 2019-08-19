# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class pdam_tangerang(models.model):
#     _name = 'pdam_tangerang.pdam_tangerang'

#     name = fields.char()
#     value = fields.integer()
#     value2 = fields.float(compute="_value_pc", store=true)
#     description = fields.text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100