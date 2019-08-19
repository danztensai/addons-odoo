# -*- coding: utf-8 -*-
from odoo import http

# class InventoryIndosis(http.Controller):
#     @http.route('/inventory_indosis/inventory_indosis/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_indosis/inventory_indosis/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_indosis.listing', {
#             'root': '/inventory_indosis/inventory_indosis',
#             'objects': http.request.env['inventory_indosis.inventory_indosis'].search([]),
#         })

#     @http.route('/inventory_indosis/inventory_indosis/objects/<model("inventory_indosis.inventory_indosis"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_indosis.object', {
#             'object': obj
#         })