# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
import logging

_logger = logging.getLogger(__name__)

class AccountingCashFlowReportWizard(models.TransientModel):

    _name = "cashflow.report.wizard"

    init_bal = fields.Integer(string="Initial Balance",required=True,default=0)
    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)

    @api.multi
    def get_report(self):
        report_obj = self.env['report']
        template = 'accounting_cashflow.cashflow_report_view'
        report = report_obj._get_report_from_name(template)

        domain = {
            'init_bal': self.init_bal,
            'date_start': self.date_start,
            'date_end': self.date_end,
        }

        vals = {
            'ids': self.ids,
            'model': report.model,
            'form': domain
        }

        """get_action() otomatis akan memanggil render_html() di report"""
        return report_obj.get_action(self, template, data=vals)

class ReportAttendanceCustom(models.AbstractModel):

    _name = 'report.accounting_cashflow.cashflow_report_view'
    _template = 'accounting_cashflow.cashflow_report_view'

    @api.model
    def render_html(self, docids, data=None):
        if data is None:
            return

        init_bal = data['form']['init_bal']
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']

        income_investing = 0
        expense_investing = 0
        net_operation = 0
        income_operation = 0
        expense_operation = 0
        net_investing = 0

        report_obj = self.env['report']

        operations = self._get_cashflow_data(init_bal,date_start, date_end,'operations')
        if operations:
            income_operation = operations[0].get('income_cashflow_type')
            expense_operation = operations[0].get('expense_cashflow_type')
            net_operation = operations[0].get('net_cashflow_type')


        investing = self._get_cashflow_data(init_bal, date_start, date_end, 'investing')
        if investing:
            income_investing = investing[0].get('income_cashflow_type')
            expense_investing = investing[0].get('expense_cashflow_type')
            net_investing = investing[0].get('net_cashflow_type')


        financing = self._get_cashflow_data(init_bal, date_start, date_end, 'financing')
        if financing:
            income_financing = financing[0].get('income_cashflow_type')
            expense_financing = financing[0].get('expense_cashflow_type')
            net_financing = financing[0].get('net_cashflow_type')

        LOCAL_FORMAT = '%d/%m/%Y'

        net_increase_in_cash = net_operation+net_investing+net_financing
        cash_end_year = net_increase_in_cash+init_bal

        vals = {
            'operations': operations,
            'init_bal' : init_bal,
            'income_operation': float(income_operation),
            'expense_operation': float(expense_operation),
            'net_operation': net_operation,
            'investing': investing,
            'income_investing' : income_investing,
            'expense_investing' : expense_investing,
            'net_investing' : net_investing,
            'financing' : financing,
            'income_financing' : income_financing,
            'expense_financing' : expense_financing,
            'net_financing' : net_financing,
            'net_increase_incash': net_increase_in_cash,
            'cash_end_year': cash_end_year,
            'date_start': datetime.strptime(date_start, DATE_FORMAT).strftime(LOCAL_FORMAT),
            'date_end': datetime.strptime(date_end, DATE_FORMAT).strftime(LOCAL_FORMAT),
        }

        return report_obj.render(self._template, values=vals)

    @api.multi
    def _get_cashflow_data(self,init_bal, date_start, date_end,cashflow_type):
        """
        return [
            {
                'employee': "employee 1 name",
                'presensi': count_of_presence,
                'absensi': count_of_absence,
            },
            {
                'employee': "employee 2 name",
                'presensi': count_of_presence,
                'absensi': count_of_absence,
            }
        ]
        """

        date_start_obj = datetime.strptime(date_start, DATE_FORMAT).date()
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT).date()

        _logger.info("Balance : "+str(init_bal))
        _logger.info(date_start_obj)
        _logger.info(date_end_obj)

        data = []
        #
        # # get all employee_data
        # employees = self.env['hr.employee'].search([], order='name asc')
        # for employee in employees:
        #     attendance_count = self.env['hr.attendance'].search_count([
        #         ('employee_id', '=', employee.id),
        #         ('check_in', '>=', date_start),
        #         ('check_in', '<=', date_end)
        #     ])
        #
        #     selisih = date_count - attendance_count
        #
        #     data.append({
        #         'employee': employee.name,
        #         'presensi': str(attendance_count) if attendance_count > 0 else '-',
        #         'absensi': str(selisih) if selisih > 0 else '-'
        #     })

        operationData = []
        coa = self.env['account.account'].search([['cashflow_type','like',str(cashflow_type)]])
        # coaFinancing = self.env['account.account'].search([['cashflow_type', 'like', 'financing']])
        # coaInvesting = self.env['account.account'].search([['cashflow_type', 'like', 'investing']])

        netCashflowType = 0.0
        incomeCashflow_type = 0.0
        expenseCashflow_type = 0.0

        for o in coa:
            _logger.info(o.name)
            coa = {}
            coa["name"]=str(o.code)+" "+ str(o.name)
            coa_income = 0.0
            coa_expense = 0.0
            journal_items_financing = self.env['account.move.line'].search([['account_id','=',o.id]])
            for jif in journal_items_financing:
                coa_income += jif.credit
                coa_expense += jif.debit

                incomeCashflow_type += jif.credit
                expenseCashflow_type += jif.debit
            coa["income"] = coa_income

            coa["expense"] = coa_expense * -1

            operationData.append(coa)

        _logger.info(operationData)
        netCashflowType = incomeCashflow_type - expenseCashflow_type

        _logger.info("Net Operation :"+str(netCashflowType))
        _logger.info("Cash Receipt From Operation : "+str(incomeCashflow_type))
        _logger.info("Cash Paid To Operation      : "+str(expenseCashflow_type))
        _logger.info(operationData)


        if operationData:
            operationData[0].update({'net_cashflow_type':netCashflowType})
            operationData[0].update({'income_cashflow_type': incomeCashflow_type})
            operationData[0].update({'expense_cashflow_type': expenseCashflow_type})

        _logger.info(operationData)

        return operationData

