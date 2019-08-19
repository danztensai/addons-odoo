# -*- coding: utf-8 -*-
{
    'name': "PDAM Tanggerang",

    'summary': """
        Custom Module Untuk PDAM Tanggerang""",

    'description': """
        Untuk kebutuhan PDAM Tanggerang
        
    """,

    'author': "Indosis Integrasi",
    'website': "https://sisintegrasi.co.id/",
    'images': ['static/src/img/icon.png'],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Application',
    'version': '0.1',

    'application' : True,

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','hr_expense','hr','hr_contract','account_accountant','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}