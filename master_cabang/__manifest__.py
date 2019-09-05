# -*- coding: utf-8 -*-
{
    'name': "Master Cabang",
    'summary': """
        Master Cabang""",
    'description': """
        Fungsi dari modul Master Cabang ini adalah:
    """,
    'author': "Ibrahim - Matrica Consulting",
    'website': "http://www.matrica.co.id",
	'application' : False,
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['hr'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/cabang_views.xml',
        'views/menu.xml',
    ],
#     only loaded in demonstration mode
#    'demo': [
#        'demo/demo.xml',
#    ],
}