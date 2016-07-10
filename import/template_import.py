#! /usr/bin/env python
# -*- coding: utf-8 -*-
# © 2016 Antonio Espinosa - <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"""
Odoo __CUSTOMER__ import from DBF (__PROGRAM__ : __FILENAME__.dbf)
"""

import os
import sys
# import textwrap

sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                '/../../common/odoo-migration-scripts')
from etl import Importer, CliBase
from etl import verbose

# Enable for custom debug
# from pprint import pformat
from collections import OrderedDict

# Import customer data mapping
# import customer


class CustomImporter(Importer):
    parser_name = 'dbf'

    # Odoo model where search/create/update
    main_model = 'res.partner'
    # Data mapping for search/create
    main_create_mapping = OrderedDict([
        ('name', {'fields': 'CNOMCLI', 'filter': 'stringify'}),
    ])
    # Data mapping for update
    main_update_mapping = OrderedDict([
        ('name', {'fields': 'CNOMCLI', 'filter': 'stringify'}),
    ])
    # Fields to read from found record
    main_read_fields = ['name']
    # Fields to avoid updating if empty value mapped ('', False, 0)
    unassigned_fields = []
    # Mandatory fields in item
    mandatory_fields = ['CCODCLI', 'CNOMCLI']

    # Un-comment this to avoid creation of new records, just update
    # avoid_create = True

    def item_query_get(self, n, item, mapping):
        """Query(s) for searching this item in Odoo DB"""
        # Use case 1: Simple one query
        # return [('name', '=', mapping['name'])]

        # Use case 2: Queries cascade, stop at first matched query
        # queries = []
        # name = mapping['name']
        # # 1. Try matching by fullname
        # queries.append([('name', '=', name)])
        # short = name.decode('utf-8')[:40].encode('utf-8')
        # if short != name:
        #     # 2. Try matching by first 40 characters of name
        #     queries.append([('name', '=', short)])
        # return queries
        return [('name', '=', mapping['name'])]

    def item_show(self, item_id, item, mapping, current={}):
        """How to show found Odoo record in console"""
        return '%s' % mapping['name']

    def item_create_post_mapping(self, n, item, mapping, current={}):
        """Mapping adjustments before search/create
        """
        # Changes over mapping dictionary
        #  ...
        return mapping

    def item_update_post_mapping(self, n, item_id, item, mapping, current={}):
        """Mapping adjustments after search/create and before update record
        """
        # Changes over mapping dictionary
        #  ...
        # N. Garbage recolected from filters, goes to comment
        garbage = mapping.get('_garbage', False)
        if garbage:
            mapping = self.garbage_add('comment', mapping, garbage)
        return mapping

    def item_check(self, n, item):
        """Check item read for integrity

        - return True, if item is valid
        - return False, if item is not valid
        """
        result = super(CustomImporter, self).item_check(n, item)
        # Custom validations here
        # if result:
        #   code = self.filter_integer_normalize(item, 'CCODCLI', 0)
        #     if code < 1000:
        #         verbose.error("Code (%d) is too old" % code, 1)
        #         return False

        # Special use case: In scripts with odoo parser when we want
        #   to iterate over read items, just to perform an action.
        #   Then, use this method to perfom the action and return False
        #         to avoid execution of search/create/update flow
        return result

    def models_load(self):
        """Load auxiliar models and data"""
        # Use case 1: Load customer mappings
        # verbose.info('Loading manual AHK mappings')
        # self.manual_model_load(ahk.amas_languages, 'res.lang', 'code')

        # Use case 2: Load auxiliar models in cache from file
        # if os.path.exists(self.options.kunde):
        #     verbose.info('Reading KUNDE file: %s' %
        #                  self.options.kunde)
        #     self.many2one_model_load('amas.kunde', 'AD_NR',
        #                              self.options.kunde, 'dbf',
        #                              ['AD_NR'])
        # else:
        #     raise Exception('Kunde file needed, use -k option')

        # Use case 3: Personalize Odoo parser
        # self.config['parsers']['odoo']['model'] = 'res.partner'
        # self.config['parsers']['odoo']['domain'] = [
        #     ('membership_start', '=', False)
        # ]
        # self.config['parsers']['odoo']['fields'] = [
        #     'id', 'name', 'membership_start', 'membership_stop',
        #     'membership_signup', 'membership_withdrawal'
        # ]

        return True

    def item_related_data(self, n, item_id, item, mapping):
        """Operation related with this Odoo record already created/updated"""
        # avoid = [
        #     'ES43 1100 2233 4455 6677 8899',
        #     'ES44 1101 2233 4455 6677 8899',
        #     'ES45 1102 2233 4455 6677 8899',
        # ]
        # # Add bank accounts to partner
        # # reading from auxiliar cached model: facturaplus.bank
        # bank_accounts = self.model_read('facturaplus.bank', item['CCODCLI'])
        # if bank_accounts:
        #     for account in bank_accounts:
        #         iban_number = self.filter_iban_check(account, 'CIBAN', False)
        #         if iban_number and not iban_number in avoid:
        #             self.partner_bank_account_add(item_id, iban_number)
        return True


# Use case: Custom CLI parameters
# class CustomCli(CliBase):
#    def usage_get(self):
#        # Born to be inherit
#        program = os.path.basename(sys.argv[0])
#        usg = """\
#            usage: %s -h | [-c CONFIG] [-v VERBOSE] [-m MAX] [-s START]
#                           [-d] [-b BancosCl.dbf] file
#
#        """
#        usg = textwrap.dedent(usg) % program
#        return usg
#
#    def doopts(self):
#        optparser = super(CustomCli, self).doopts()
#        optparser.add_option('-b', '--banks', dest='banks',
#                             metavar='BancosCl.dbf', default='',
#                             help='DBF file with IBAN partner accounts')
#        return optparser


def main():
    # Use case 1: Use standard CLI
    cli = CliBase('template_import', '1.0')
    # Use case 2: Use custom CLI
    # cli = CustomCli('template_import', '1.0')
    importer = CustomImporter(cli.args, cli.options, cli.config)

    cli.run(importer, verbose.INFO)

if __name__ == '__main__':
    main()
