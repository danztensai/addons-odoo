# -*- coding: utf-8 -*-
from odoo import http

# class AccountingCashflow(http.Controller):
#     @http.route('/accounting_cashflow/accounting_cashflow/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/accounting_cashflow/accounting_cashflow/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('accounting_cashflow.listing', {
#             'root': '/accounting_cashflow/accounting_cashflow',
#             'objects': http.request.env['accounting_cashflow.accounting_cashflow'].search([]),
#         })

#     @http.route('/accounting_cashflow/accounting_cashflow/objects/<model("accounting_cashflow.accounting_cashflow"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('accounting_cashflow.object', {
#             'object': obj
#         })