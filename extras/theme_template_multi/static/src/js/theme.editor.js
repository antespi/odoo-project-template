/**
 * # -*- coding: utf-8 -*-
 * © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html
 */

(function(){
    'use strict';

    var website = openerp.website;
    var session_editor = new openerp.Session();
    var _t = openerp._t;

    website.openerp_website = {};

    if ($('html.template').length > 0) {

        /* Load customize modal
        openerp.jsonRpc('/web/dataset/call', 'call', {
                'model': 'ir.ui.view',
                'method': 'read_template',
                'args': ['theme_template_multi.theme_customize', openerp.website.get_context()]
            }).done(function (data) {
            openerp.qweb.add_template(data);
        });

        website.ready().done(function() {
            website.Theme = website.Theme.extend({
                template: 'theme_template_multi.theme_customize'
            });
        });
        */

        /* Inherit snippets options
        website.snippet.options.marginAndResize.include({
            start: function () {
                this._super.apply(this, arguments);
                // Do your stuff
            },
            my_new_method: function () {
                // Do your stuff
            }
        });
        */

        /* New snippet options
        website.snippet.options.my_snippet = website.snippet.Option.extend({
            selector : ".top_banner *",
            start: function() {
                // Do your staff
            }
        });
        */

        // Called when the HTML-Document is loaded and the DOM is ready,
        // even if all the graphics haven’t loaded yet
        $(document).ready(function() {
            // Do your staff
        });

        // Called when the complete page is fully loaded, including
        // all frames, objects and images
        $(window).load(function() {
            // Do your staff
        });
    } // if $('html.template')

})();
