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

    # customer_status = fields.Selection(
    #     [('approved', 'Approved'),
    #      ('pending', 'Pending'),
    #      ('denied', 'Tolak')],
    #     'Status Approval', default='pending')
    state = fields.Selection(
        [('entry','Entry data'),('survey', 'Survey'),('validate', 'Validasi'), ('approved', 'Diterima'),('denied', 'Tolak')],string="Status Pendaftaran Pelanggan",default='entry')
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
    status_id = fields.Many2one('pdam_tangerang.status.pelanggan', ondelete='set null', string="Status Pelanggan", index=True)
    penggunaan_air = fields.Char(string="Penggunaan Air")
    luas_bangunan = fields.Char(string="Luas Bangunan")
    jumlah_jiwa = fields.Char(string="Jumlah Jiwa")
    wilayah_pasang = fields.Char(string="Wilayah Pasang")
    registration = fields.Boolean(store=True)
    pipe_tapping_diameter = fields.Char(string="Tapping Dari Pipa Diameter")
    status_bangunan = fields.Char(string="Status Bangunan")

    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        record = super(ResPartner, self).create(values)

        # Change the values of a variable in this super function
        record['registration_number'] =  self.env['ir.sequence'].get('res.partner') or '/'
        record['registration'] = False

        return record

    @api.multi
    def action_done(self):
        self.ensure_one()
        self.write({'registration': True})
        return self.write({'state': 'approved'})

        # return {
        #     # 'name': _('Daftar Kebutuhan Barang'),
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'pdam_tangerang.dkb',
        #     'view_id': False,
        #     'type': 'ir.actions.act_window',
        #     'target': 'current',
        #     'nodestroy': True
        # }


    @api.multi
    def action_survey(self):
        self.ensure_one()
        self.write({'registration': False})
        return self.write({'state': 'survey'})

    @api.multi
    def action_denied(self):
        self.ensure_one()
        return self.write({'state': 'denied'})

    @api.multi
    def action_validasi(self):
        self.ensure_one()
        return self.write({'state': 'validate'})


class StatusPelanggan(models.Model):
    _name='pdam_tangerang.status.pelanggan'

    name = fields.Char(string="Status Pelanggan",required=True)
    description  = fields.Char(string="Keterangan Status Pelanggan")

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

class Survey(models.Model):
    _name = 'pdam_tangerang.survey'

    name = fields.Char("Nama",compute="_survey_name")

    wilayah_id = fields.Many2one('pdam_tangerang.wilayah',ondelete='set null', string="Wilayah",index=True)
    employee_id = fields.Many2one('hr.employee', ondelete='set null', string="Nama Petugas", index=True)
    survey_date = fields.Date(string="Tanggal Survey",required=True,default=fields.Date.today)
    customer_id = fields.Many2one('res.partner',ondelete='set null',string="Nama Pelanggan",index=True)
    registration_number = fields.Char(string='No Pendaftaran', related='customer_id.registration_number')
    pipe_length = fields.Float(string="Panjang Pipa")
    pipe_diameter = fields.Float(string="Diameter Pipa")
    resident_count = fields.Integer(string="Jumlah Penghuni")
    lb_survey = fields.Char(string="LB Survey")
    fee_group = fields.Char(string="Gol. Tarif")
    state = fields.Selection([('survey','Survey'),('verified','Verifikasi'),('denied','Tolak')],'Status Survey',default='survey')
    house_image = fields.Binary(string="Foto Rumah")
    color = fields.Integer('Warna')

    @api.depends('employee_id','wilayah_id','customer_id', 'registration_number')
    def _survey_name(self):
        self.name = self.employee_id.name+"-"+self.wilayah_id.name+"-"+self.registration_number + "-" + str(self.customer_id.name)

    @api.multi
    def action_done(self):
        self.ensure_one()
        self.write({'state': 'verified'})
        return {
            # 'name': _('Daftar Kebutuhan Barang'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pdam_tangerang.dkb',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'nodestroy': True
        }

    @api.multi
    def action_survey(self):
        self.ensure_one()
        return self.write({'state': 'survey'})

    @api.multi
    def action_denied(self):
        self.ensure_one()
        return self.write({'state': 'denied'})

class Dkb(models.Model):
    _name = 'pdam_tangerang.dkb'

    name = fields.Char(string="Keterangan",compute="_dkb_name", store=True)
    customer_id = fields.Many2one('res.partner',required=True,string="Nama Pelanggan",index=True)
    registration_number = fields.Char(string='Nomor Pendaftaran',related='customer_id.registration_number')
    customer_address = fields.Char(string="Alamat Pemasangan",related='customer_id.street')
    status_pemasangan_id = fields.Many2one('pdam_tangerang.status.pemasangan',string="Status Pemasangan",default=1)
    additional_pipe_length = fields.Integer(string="Penambahan Pipa")
    barang_id_line = fields.One2many('pdam_tangerang.dkb.line','dkb_id', string="Barang")

    @api.depends('customer_id', 'registration_number')
    def _dkb_name(self):
        self.name = self.registration_number+"-"+str(self.customer_id.name)

class DkbLine(models.Model):
    _name='pdam_tangerang.dkb.line'

    name = fields.Char(string="Keterangan")
    dkb_id = fields.Many2one('pdam_tangerang.dkb')
    barang_id = fields.Many2one('product.product',string="Barang")
    product_uom_qty = fields.Float(string='Jumlah', required=True,
                                   default=1.0)
    product_uom = fields.Many2one('product.uom', string='Satuan', required=True)

class StatusPemasangan(models.Model):
    _name = 'pdam_tangerang.status.pemasangan'

    name = fields.Char(string="Status")
    description = fields.Char(string="Penjelasan Status")








