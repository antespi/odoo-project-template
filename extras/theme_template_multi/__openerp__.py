# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Template theme multi",
    "summary": "Template theme with multi-website support",
    "version": "8.0.1.0.0",
    "category": "Theme/Corporate",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_multi_theme",
        "theme_base",
    ],
    "data": [
        "data/website_theme.xml",
        "views/assets.xml",
        # Optional configuration
        # "views/options.xml",
        # "views/customize_modal.xml",
        # "views/images_library.xml",
        # "views/snippets.xml",
        # "views/snippets_options.xml",
        # "views/pages.xml",
        # "views/menus.xml",
    ],
    'qweb': [
        # 'static/src/xml/s_sample_modal.xml',
    ],
}
