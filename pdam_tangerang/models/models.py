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

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ktp_no = fields.Char(
        string="No KTP",  # Optional label of the field
        help = 'No KTP Pelanggan',  # Help tooltip text
        company_dependent = True,  # Transform columns to ir.property
        search = '_search_function'  # Custom search function mainly used with compute
    )
    npwp_no = fields.Char(
        string="No NPWP",  # Optional label of the field
        help='Nomor NPWP Pelanggan',  # Help tooltip text
        company_dependent=True,  # Transform columns to ir.property
        search='_search_function'  # Custom search function mainly used with compute
    )

    kk_image = fields.Binary(string="Upload Foto Kartu Keluarga")
    ktp_image = fields.Binary(string="Upload Foto KTP")
    registration_number = fields.Char(string="No Pendaftaran")
    spl_date = fields.Date(string="Tanggal SPL", required=True,default=fields.Date.today)

    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        record = super(ResPartner, self).create(values)

        # Change the values of a variable in this super function
        record['registration_number'] =  self.env['ir.sequence'].get('res.partner') or '/'

        return record

class Wilayah(models.Model):
    _name = 'pdam_tangerang.wilayah'

    name = fields.Char(string="Wilayah",help="Nama Wilayah",required=True)
    description = fields.Char(string="Keterangan")

# Kelas untuk Model Surat Perintah Kerja Opname (SPKO)
class Spko(models.Model):
    _name = 'pdam_tangerang.spko'


    wilayah_id = fields.Many2one('pdam_tangerang.wilayah', ondelete='set null', string="Wilayah", index=True)
    employee_id = fields.Many2one('hr.employee', ondelete='set null', string="Nama Petugas", index=True)
    customer_id = fields.Many2one('res.partner',ondelete='set null',string="Nama Pelanggan",index=True)
    registration_number = fields.Char(string='No Pendaftaran',related='customer_id.registration_number')
    installation_address = fields.Char(string="Alamat Pemasangan",related='customer_id.street')
    spko_detail = fields.Char(String="Keterangan")
