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

import werkzeug
import werkzeug.urls

from openerp import http
from openerp.http import request
from openerp.tools.translate import _


class MyController(http.Controller):

    available_fields = []
    required_fields = []

    def available_fields_get(self):
        """ Allow to be overrided """
        self.available_fields = ['field_one', 'field_two']

    def required_fields_get(self):
        """ Allow to be overrided """
        self.required_fields = ['field_one']

    def values_get(self, kwargs):
        """ Allow to be overrided """
        values = {}
        for field in self.available_fields:
            if kwargs.get(field, None) is not None:
                values[field] = kwargs.pop(field)
        return values

    def create_lead(self, values, kwargs):
        """ Allow to be overrided """
        return request.registry['crm.lead'].with_context(
            mail_create_nosubscribe=True).sudo().create(values)

    def form_render(self, values, kwargs):
        """ Allow to be overrided """
        # Metadata
        values['_available_fields'] = self.available_fields
        values['_required_fields'] = self.required_fields
        # Render form
        return request.website.render(
            "sample_website_addon.my_controller_form", values)

    def result_ok(self, values, kwargs):
        """ Allow to be overrided """
        return request.website.render(
            "sample_website_addon.my_controller_ok", values)

    def my_controller_check(self, values):
        """ Allow to be overrided """
        error = set(field for field in self.required_fields
                    if not values.get(field))
        return error

    @http.route(['/my-controller'], type='http', auth="public", website=True)
    def my_controller_form(self, **kwargs):
        values = self.values_get(kwargs)
        return self.form_render(values, kwargs)

    @http.route(['/crm/my-controller'], type='http', auth="public",
                website=True)
    def my_controller(self, **kwargs):
        values = self.values_get(kwargs)
        # Check input data
        error = self.my_controller_check(values)
        if error:
            # If error, show form again with errors
            values = dict(values, error=error)
            return self.form_render(values, kwargs)
        # If validated, create a new lead
        self.create_lead(values, kwargs)
        # Show OK and thanks to user
        return self.result_ok(values, kwargs)
