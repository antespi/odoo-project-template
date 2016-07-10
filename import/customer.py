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
Facturaplus auxiliar data
"""

fp_countries = {
    'ESPA' : [False, 'ES'],
    'PORT' : [False, 'PT'],
    'FRAN' : [False, 'FR'],
    'HOL'  : [False, 'NL'],
    'MARR' : [False, 'MA'],
    'USA'  : [False, 'US'],
    'RU'   : [False, 'RU'],
}
fp_agents = {
    '01' : [False, ''],
}

fp_payments = {
    # FacturaPlus Payment : [mode, term]
    '01' : [(False, 'Talón'), (False, '30 días')], # T/30 DIAS FF
    '02' : [(False, 'Talón'), (False, '30 días - Vencimiento 10-25')], # T/30 VTO.10-25
    '07' : [(False, 'Talón'), (False, '60 días - Vencimiento 10-25')], # T/60VTO. 10-25
    '08' : [(False, 'Giro domiciliado SEPA 5801'), (False, '30 días - Vencimiento 15')], # L/30 DIAS VTO 15
    '10' : [(False, 'Giro domiciliado SEPA 5801'), (False, '60 días')], # L/60 DIAS
    '12' : [(False, 'Giro domiciliado SEPA 5801'), (False, '60 días - Vencimiento 30')], # L/60 DIAS VTO.30
    '15' : [(False, 'Giro domiciliado SEPA 5801'), (False, '90 días - Vencimiento 25')], # L/90 DIAS VTO.25
    '99' : [(False, 'Contado'), (False, 'Inmediato')], # CONTADO
    '23' : [(False, 'Giro domiciliado SEPA 5801'), (False, '85 días - Vencimiento 10-25')], # L/A 85 DIAS VTO.10-25
    '13' : [(False, 'Giro domiciliado SEPA 5801'), (False, '60 días')], # L/60DIAS F.F
    '25' : [(False, 'Giro domiciliado SEPA 5801'), (False, '30 días - Vencimiento 25')], # T/30 VTO. 25
    '27' : [(False, 'Pagaré'), (False, '60 días - Vencimiento 20')], # PAGARE 60 DIAS VTO.20
    '28' : [(False, 'Pagaré'), (False, '90 días')], # PAGARE 90 DIAS F.F
    '29' : [(False, 'Pagaré'), (False, '90 días - Vencimiento 15')], # PAGARE 90 DIAS VTO.15
    '38' : [(False, 'Pagaré'), (False, '90 días - Vencimiento 10')], # PAGARE 90 DIAS VTO.10
    '97' : [(False, 'Pagaré'), (False, '50% Inmediato - 50% 120 días')], # 1/2CONT- PAG 120
    '42' : [(False, 'Pagaré'), (False, '45 días')], # PAGARE 45 DIAS F.F
    '43' : [(False, 'Pagaré'), (False, '90 días - Vencimiento 25')], # PAGARE 90 DIAS VTO.25
    'TC' : [(False, 'Talón'), (False, '60 días - Vencimiento 30')], # T/60 VTO. 30
    '6'  : [(False, 'Talón'), (False, '60 días - Vencimiento 2-17')], # T/60 DIAS VTO 2-17
    '1'  : [(False, 'Talón'), (False, '90 días')], # T/90 DIAS FF
    'P2' : [(False, 'Pagaré'), (False, '90 días - Vencimiento 10-25')], # PAGARE 90 D VTO-10-25
    '71' : [(False, 'Talón'), (False, '60 días')], # T/60 DIAS
    'P6' : [(False, 'Talón'), (False, '60 días - Vencimiento 10-25')], # T/60 VTO. 10-25
    'CN' : [(False, 'Contado'), (False, 'Inmediato')], # CONTADO
    'C9' : [(False, 'Confirming'), (False, '90 días - Vencimiento 20')], # CONFIRMING 90DIAS VTO 20
    'ER' : [(False, 'Talón'), (False, '30 días - Vencimiento 15-30')], # T/30 VTO. 15-30
    'C6' : [(False, 'Confirming'), (False, '60 días - Vencimiento 30')], # CONFIRMING 60 VTO 30
    '2B' : [(False, 'Pagaré'), (False, '85 días - Vencimiento 5-20')], # PAGARE 85 VTO 5-20
    'AL' : [(False, 'Confirming'), (False, '30 días - Vencimiento 5')], # CONFIRMING 30 DIAS VTO 5
    'C5' : [(False, 'Confirming'), (False, '60 días - Vencimiento 27')], # CONFIRMING 60D VTO 27
    '3X' : [(False, 'Contado'), (False, '30% Adelantado - Resto Entrega')], # 30% ADELANTADO-RESTO FINALIZA
    '5W' : [(False, 'Pagaré'), (False, '60 días - Vencimiento 25')], # PAGARE 60 DIAS VTO 25
    'AF' : [(False, 'Confirming'), (False, '30 días - Vencimiento 20')], # CONFIRMING 30 VTO 20
    'MN' : [(False, 'Talón'), (False, '60 días - Vencimiento 15')], # T/60 VTO 15
    '2'  : [(False, 'Pagaré'), (False, '85 días')], # PAGARE 85 DIAS F.F
    '4'  : [(False, 'Pagaré'), (False, '70 días - Vencimiento 10-25')], # PAGARE 70 DIAS VTO. 10-25
    '5'  : [(False, 'Pagaré'), (False, '60 días - Vencimiento 15')], # PAGARE 60 DIAS VTO. 15
    '7'  : [(False, 'Pagaré'), (False, '60 días - Vencimiento 13-27')], # PAGARE 60 DIAS VTO. 13-27
    '11' : [(False, 'Pagaré'), (False, '60 días - Vencimiento 10-25')], # PAGARE 60 VTO 10-25
    '26' : [(False, 'Talón'), (False, '30 días - Vencimiento 20')], # T/30 VTO. 20
    'CO' : [(False, 'Contado'), (False, 'Inmediato')], # Contado
    'P3' : [(False, 'Pagaré'), (False, '85 días - Vencimiento 20')], # PAGARE 85 DIAS VTO 20
    '91' : [(False, 'Pagaré'), (False, '60 días')], # PAGARE 60 DIAS FF
    'P4' : [(False, 'Pagaré'), (False, '85 días - Vencimiento 15-30')], # PAGARÉ 85 DIAS VTO. 15-30
    'C4' : [(False, 'Confirming'), (False, '60 días')], # CONFIRMING 60D FF
    '22' : [(False, 'Pagaré'), (False, '60 días - Vencimiento 25')], # PAGARE 60D VTO.25
    '21' : [(False, 'Pagaré'), (False, '30-60-90 días - Vencimiento 30')], # PAG 30-60-90 VTO 30
    '5G' : [(False, 'Pagaré'), (False, '30% Adelantado - Resto 60 días')], # 30% ADEL. 70% PAG 60 D.F.F
    '35' : [(False, 'Confirming'), (False, '75 días')], # CONFIRMING 75 DIAS FF
    'C1' : [(False, 'Confirming'), (False, '60 días - Vencimiento 20')], # CONFIRMING 60 VTO. 20
    'P1' : [(False, 'Pagaré'), (False, '75 días')], # PAGARE 75 DIAS F.F.
    '46' : [(False, 'Pagaré'), (False, '30 días')], # PAGARE 30 DIAS FF
    'CF' : [(False, 'Confirming'), (False, '30 días - Vencimiento 15')], # CONFIRMING 30 DIAS VTO. 15
    '41' : [(False, 'Pagaré'), (False, '30-60-90 días')], # PAGARE 30-60-90 DIAS FF
    'C7' : [(False, 'Confirming'), (False, '60 días - Vencimiento 10-25')], # CONFIRMING 60 DIAS 10-25
    '48' : [(False, 'Pagaré'), (False, '30 días - Vencimiento 25')], # PAGARE 30 DIAS VTO 25
    'C2' : [(False, 'Confirming'), (False, '60 días - Vencimiento 5-20')], # CONFIRMING 60 DIAS 5-20
    'FP' : [(False, 'Contado'), (False, 'Inmediato')], # PAGADO
    'SG' : [(False, 'Confirming'), (False, '30 días')], # CONFIRMING 30 DIAS
    'CT' : [(False, 'Confirming'), (False, '60 días - Vencimiento 25')], # CONFIRMING 60 DIAS VTO 25
    'EF' : [(False, 'Contado'), (False, 'Entrega')], # EFECTIVO A LA ENTREGA
    'CA' : [(False, 'Contado'), (False, 'Adelantado')], # CONTADO ADELANTADO
    '6X' : [(False, 'Contado'), (False, '50% Adelantado - Resto Entrega')], # 50% ADELANTADO-50% RECOGIDA 5
    'MI' : [(False, 'Contado'), (False, 'Inmediato')], # MATERIAL-ADEL-INSTAL-CONT
    '5P' : [(False, 'Pagaré'), (False, '50% Adelantado - 50% 30 días')], # 50% adelantado-50% pagare 30
    'LC' : [(False, 'Confirming'), (False, '90 días')], # CARTA DE PAGO 90 DIAS

}
