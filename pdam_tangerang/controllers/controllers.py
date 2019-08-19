# -*- coding: utf-8 -*-
from odoo import http

# class PdamTangerang(http.Controller):
#     @http.route('/pdam_tangerang/pdam_tangerang/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pdam_tangerang/pdam_tangerang/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pdam_tangerang.listing', {
#             'root': '/pdam_tangerang/pdam_tangerang',
#             'objects': http.request.env['pdam_tangerang.pdam_tangerang'].search([]),
#         })

#     @http.route('/pdam_tangerang/pdam_tangerang/objects/<model("pdam_tangerang.pdam_tangerang"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pdam_tangerang.object', {
#             'object': obj
#         })