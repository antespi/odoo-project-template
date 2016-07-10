# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Antonio Espinosa <antonioea@antiun.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    # Theme information
    'name': "Sample Backend Theme",
    'description': """
Sample Theme
==================

Theme for Sample:

- Backend

    """,
    'category': 'Theme',
    'version': '1.0',

    # Dependencies
    'depends': [
        'web',
    ],
    'external_dependencies': {},

    # Views templates, pages, menus, options and snippets
    'data': [
        'views/backend.xml',
        'views/pages.xml',
        'views/options.xml',
        'views/snippets.xml',
        'views/menus.xml',
        'reports/common.xml',
        'reports/invoice.xml',
        'reports/picking.xml',
        'reports/purchase_order.xml',
        'reports/purchase_quotation.xml',
        'reports/sale_order.xml',
        'reports/stock_picking_wave.xml',
    ],

    # Qweb templates
    'qweb': [
        'static/src/xml/backend.xml',
    ],

    # Your information
    'author': 'Antiun Ingenieria',
    'maintainer': 'Antiun Ingenieria',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',

    # Technical options
    'demo': [],
    'test': [],
    'installable': True,
    # 'auto_install':False,
    # 'active':True,

}
