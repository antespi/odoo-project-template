#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Defining Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
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

"""
OpenERP customer import from DBF (FacturaPlus : Clientes.dbf)
"""

import os
import sys
import textwrap

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../common/odoo-migration-scripts')
from etl import Importer, CliBase
from etl import verbose
from etl.main import list_encode

import re
import time
from pprint import pformat
from collections import OrderedDict

import customer

class customer_importer(Importer):
    parser_name = 'dbf'

    main_model = 'res.partner'
    main_create_mapping = OrderedDict([
        ('name'       , {'fields' : 'CNOMCLI', 'filter' : 'stringify'}),
        ('is_company' , {'fields' : 'CDNICIF', 'filter' : 'iscompany_by_vat', 'default' : True}),
        ('vat'        , {'fields' : 'CDNICIF', 'filter' : 'vat_check', 'default' : False}),
    ])
    main_update_mapping = OrderedDict([
        ('name'       , {'fields' : 'CNOMCLI', 'filter' : 'stringify'}),
        ('is_company' , {'fields' : 'CDNICIF', 'filter' : 'iscompany_by_vat', 'default' : True}),
        ('customer'   , {'default' : True}),
        ('fp_customer', {'fields' : 'CCODCLI', 'filter' : 'stringify', 'default' : ''}),
        ('vat'        , {'fields' : 'CDNICIF', 'filter' : 'vat_check', 'default' : False}),

        ('comercial'  , {'fields' : 'CNOMCOM', 'filter' : 'stringify', 'default' : ''}),
        ('street'     , {'fields' : 'CDIRCLI', 'filter' : 'stringify', 'default' : ''}),
        ('zip'        , {'fields' : 'CPTLCLI', 'filter' : 'stringify', 'default' : ''}),
        ('city'       , {'fields' : 'CPOBCLI', 'filter' : 'stringify', 'default' : ''}),
        ('state_id'   , {'fields' : 'CCODPROV', 'filter' : 'stateid_by_provincecode', 'default' : False}),
        ('country_id' , {'fields' : 'CNACCLI', 'filter' : 'countryid_by_countrycode', 'default' : False}),
        ('zip_id'     , {'fields' : 'CPTLCLI', 'filter' : 'many2one', 'default' : False,
                        'model' : 'res.better.zip', 'query' : [('name', '=', '@CPTLCLI')], 'all' : False}),
        ('_zip_ids'   , {'fields' : 'CPTLCLI', 'filter' : 'many2one', 'default' : False,
                        'model' : 'res.better.zip', 'query' : [('name', '=', '@CPTLCLI')], 'all' : True}),

        ('phone'      , {'fields' : 'CTF01CLI', 'filter' : 'phone_normalize', 'default' : ''}),
        ('mobile'     , {'fields' : 'CTF02CLI', 'filter' : 'phone_normalize', 'default' : ''}),
        ('fax'        , {'fields' : 'CFAXCLI', 'filter' : 'phone_normalize', 'default' : ''}),
        ('email'      , {'fields' : 'EMAIL', 'filter' : 'email_check', 'default' : ''}),
        ('comment'    , {'filter' : 'append', 'separator' : '\n', 'default' : 'Migración clientes FacturaPlus %s' % time.strftime('%d/%m/%Y %H:%M:%S')}),

        ('customer_payment_mode' , {'fields' : 'CCODPAGO', 'filter' : 'paymentmodeid_by_code', 'default' : False}),
        ('property_payment_term' , {'fields' : 'CCODPAGO', 'filter' : 'paymenttermid_by_code', 'default' : False}),
        ('property_account_position' , {'filter' : 'many2one', 'default' : False,
                        'model' : 'account.fiscal.position', 'query' : [('name', '=', 'Régimen Nacional')]}),

    ])
    main_read_fields = ['name', 'is_company', 'comment']
    unassigned_fields = ['customer', 'supplier', 'ref', 'vat',
                         'street', 'zip', 'city', 'state_id', 'country_id',
                         'zip_id', 'phone', 'fax', 'email',
                         'customer_payment_mode', 'property_payment_term']
    mandatory_fields = ['CCODCLI', 'CNOMCLI']

    def countries_load(self):
        for k,v in customer.fp_countries.iteritems():
            country_id = self.model_search('res.country', [('code', '=', v[1])])
            customer.fp_countries[k] = [country_id, v[1]]

    def payments_load(self):
        for k,v in customer.fp_payments.iteritems():
            pm_id = self.model_search('payment.mode', [('name', '=', v[0][1])])
            pt_id = self.model_search('account.payment.term', [('name', '=', v[1][1])])
            customer.fp_payments[k] = [(pm_id, v[0][1]), (pt_id, v[1][1])]

    def filter_stateid_by_provincecode(self, item, fields, default=False, config={}, mapping={}):
        value = self.filter_stringify(item, fields, '', config, mapping)
        if re.match(r'^00[0-9]{2}$', value):
            # Search OpenERP state by code
            code = value[2:]
            state_id = self.model_search('res.country.state', [('code', '=', code)])
            if state_id: return state_id

        return default

    def filter_countryid_by_countrycode(self, item, fields, default=False, config={}, mapping={}):
        value = self.filter_stringify(item, fields, '', config, mapping)
        if value in customer.fp_countries:
            return customer.fp_countries[value][0]
        return default

    def filter_paymentmodeid_by_code(self, item, fields, default=False, config={}, mapping={}):
        value = self.filter_stringify(item, fields, '', config, mapping)
        # payment = self.model_read('facturaplus.payment', value)
        # if payment and payment['CDESCPAGO'] in self.fp_payments:
        if value in customer.fp_payments:
            return customer.fp_payments[value][0][0]
        return default

    def filter_paymenttermid_by_code(self, item, fields, default=False, config={}, mapping={}):
        value = self.filter_stringify(item, fields, '', config, mapping)
        # payment = self.model_read('facturaplus.payment', value)
        # if payment and payment['CDESCPAGO'] in self.fp_payments:
        if value in customer.fp_payments:
            return customer.fp_payments[value][1][0]
        return default

    def filter_vat_normalize(self, item, fields, default=False, config={}, mapping={}):
        value = super(customer_importer, self).filter_vat_normalize(item, fields, default, config, mapping)

        # Read country code from item, default ES
        nac = item['CNACCLI'] if 'CNACCLI' in item and item['CNACCLI'] else 'ESPA'
        country = ''
        if nac in customer.fp_countries:
            country = customer.fp_countries[nac][1]
        # If VAT does not have country code, add country code
        if value and not re.match(r'^[A-Z]{2}', value):
            value = country + value

        return value

    def filter_email_check(self, item, fields, default='', config={}, mapping={}):
        value = self.filter_string_nospaces(item, fields, default, config, mapping)
        clean = super(customer_importer, self).filter_email_check(item, fields, default, config, mapping)
        if value and not clean:
            if not '_garbage' in mapping: mapping['_garbage'] = []
            mapping['_garbage'].append('EMAIL: %s' % value)

        return clean


    def item_query_get(self, n, item, mapping):
        queries = []
        name = mapping['name']
        # Try matching by fullname
        queries.append([('name', '=', name)])
        short = name.decode('utf-8')[:40].encode('utf-8')
        if short != name:
            # Try matching by first 40 characters of name
            queries.append([('name', '=', short)])
        vat = mapping['vat'] if 'vat' in mapping else False
        if vat:
            # Try matching by vat
            queries.append([('vat', '=', vat)])
        no_coma = re.sub(r'[,]', '', mapping['name'])
        if no_coma != name:
            # Try matching without coma
            queries.append([('name', '=', no_coma)])
        no_title = re.sub(r',?\s?S\.[AL]\.?$', '', mapping['name'])
        # Try matching without S.L or S.A
        queries.append([('name', 'ilike', no_title)])
        return queries

    def item_show(self, item_id, item, mapping):
        # Inherit this method to change search query
        return '%s' % mapping['name']

    def item_update_post_mapping(self, n, item_id, item, mapping):
        # Update mapping post-processing
        zip_ids = mapping.pop('_zip_ids', False)
        zipcode = mapping['zip']
        zipdata = None
        garbage = []
        # Load res.better.zip, if not loaded
        self.model_get('res.better.zip')
        # Pre-load Spain country_id
        spain_id = self.model_search('res.country', [('code', '=', 'ES')])
        # 1. Heuristic for zip, city, state and country. Only for unknown or Spain country
        if not mapping['country_id'] or mapping['country_id'] == spain_id:
            if zip_ids:
                zip_id = zip_ids[0]
                zipdata = self.model_read('res.better.zip', zip_id, ['city', 'state_id', 'country_id'])

            if zipdata:
                # Get info from better zip
                if len(zip_ids) == 1:
                    if mapping['city']: garbage.append('POBLACION: %s' % mapping['city'])
                    mapping['city'] = zipdata['city']
                    mapping['zip_id'] = zip_id
                    # print 'zipdata : Setting city (%s) and zip_id (%d)' % (zipdata['state_id'][0], zipdata['country_id'][0])
                mapping['state_id'] = int(zipdata['state_id'][0])
                if item['CNACCLI']: garbage.append('PAIS: %s' % item['CNACCLI'])
                mapping['country_id'] = spain_id
                # print 'zipdata : Setting state_id (%s) and country_id (%s)' % (zipdata['state_id'][0], zipdata['country_id'][0])
            elif zipcode and re.match(r'^[0-9]{5}$', zipcode):
                # Get info from spanish zipcode
                code = zipcode[0:2]
                mapping['state_id'] = self.model_search('res.country.state', [('code', '=', code)])
                if item['CNACCLI']: garbage.append('PAIS: %s' % item['CNACCLI'])
                mapping['country_id'] = spain_id

        # 2. Heuristic for state and country
        if mapping['state_id'] and not mapping['country_id']:
            state = self.model_read('res.country.state', mapping['state_id'], 'country_id')
            if state:
                if item['CNACCLI']: garbage.append('PAIS: %s' % item['CNACCLI'])
                mapping['country_id'] = state['country_id'][0]

        # If there is garbage from heuristic #1 or #2
        if garbage:
            # print pformat(garbage)
            if mapping['comment']: garbage = [mapping['comment']] + garbage
            mapping['comment'] = ' - '.join(list_encode(garbage))
            # print mapping['comment']

        # N. Garbage recolected from filters, goes to comment
        garbage = mapping.pop('_garbage', False)
        if garbage:
            if mapping['comment']: garbage = [mapping['comment']] + garbage
            mapping['comment'] = ' - '.join(list_encode(garbage))
        return mapping

    # def item_check(self, n, item):
    #     if not super(customer_importer, self).item_check(n, item):
    #         print 'item = ' + pformat(item)
    #
    #     return False

    def models_load(self):
        self.countries_load()
        self.payments_load()

        if os.path.exists(self.options.banks):
            # print 'Banks file : %s' % self.options.banks
            self.many2one_model_load('facturaplus.bank', 'CCODCLI', self.options.banks, 'dbf', ['CIBAN'])

        # if os.path.exists(self.options.provinces):
        #     # print 'Provinces file : %s' % self.options.provinces
        #     self.many2one_model_load('facturaplus.province', 'CCODPROV', self.options.provinces, 'dbf', ['CNOMPROV'])

        # if os.path.exists(self.options.payments):
        #     # print 'Provinces file : %s' % self.options.provinces
        #     self.many2one_model_load('facturaplus.payment', 'CCODPAGO', self.options.payments, 'dbf', ['CDESCPAGO'])

        return True

    def item_related_data(self, n, item_id, item, mapping):
        self._current_related = []
        avoid = [
            'ES61 2100 5706 8102 0000 5801',
            'ES55 0049 4475 6124 1000 9346',
            'ES70 0075 0314 1606 0200 7933',
            'ES87 0128 0087 1205 0000 7777',
            'ES49 0049 4475 6126 9000 4901',
        ]

        # Add bank accounts to partner
        bank_accounts = self.model_read('facturaplus.bank', item['CCODCLI'])
        if bank_accounts:
            for account in bank_accounts:
                iban_number = self.filter_iban_check(account, 'CIBAN', False)
                if iban_number and not iban_number in avoid:
                    self.partner_bank_account_add(item_id, iban_number)

        return True

    # def item_write(self, n, item_id, item, mapping):
    #     verbose.show(verbose.INFO, "Writing ID " + str(item_id) + " : " + pformat(mapping))

class customer_cli(CliBase):
    def usage_get(self):
        # Born to be inherit
        program = os.path.basename(sys.argv[0])
        usg = """\
                    usage: %s -h | [-c CONFIG] [-v VERBOSE] [-m MAX] [-d] [-b BancosCl.dbf] file

                    """
        usg = textwrap.dedent(usg) % program
        return usg

    def doopts(self):
        optparser = super(customer_cli, self).doopts()

        optparser.add_option('-b', '--banks', dest='banks',
                                            metavar='BancosCl.dbf', default='',
                                            help='DBF file with IBAN partner accounts')

        # optparser.add_option('-p', '--provinces', dest='provinces',
        #                                     metavar='Provinc.dbf', default='',
        #                                     help='DBF file with province codes')

        # optparser.add_option('-f', '--payments', dest='payments',
        #                                     metavar='FPago.dbf', default='',
        #                                     help='DBF file with payment modes')

        return optparser


def main():
    cli = customer_cli('customer_customer_facturaplus_importer', '1.0')
    importer = customer_importer(cli.args, cli.options, cli.config)

    cli.run(importer, verbose.INFO)

if __name__ == '__main__':
    main()
