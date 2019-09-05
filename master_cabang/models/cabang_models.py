# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError, ValidationError
from openerp.exceptions import except_orm, Warning, RedirectWarning
from datetime import date, datetime, timedelta

class master_cabang(models.Model):
    _name = 'master.cabang'
    _description = 'Master Cabang'

    name        = fields.Char('Nama Cabang')