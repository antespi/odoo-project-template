/**
 * # -*- coding: utf-8 -*-
 * © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html
 */

(function(){
    'use strict';

    var website = openerp.website;
    var session = new openerp.Session();
    var _t = openerp._t;

    website.openerp_website = {};

    if ($('html.template').length > 0) {

        /* New snippet animation
        website.snippet.animationRegistry.my_snippet = website.snippet.Animation.extend({
            selector : ".top_banner *",
            start: function() {
                // Do your staff
            },
            stop: function() {
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
