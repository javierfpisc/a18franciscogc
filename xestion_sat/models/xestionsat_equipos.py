# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, api

class XestionsatEquipos(models.Model):
    _name = 'xestionsat.equipos'
    _description = 'XestionSAT Equipos'
    _order = 'partner_id, data_alta'
    
    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    sede_id = fields.Many2one('res.partner', string='Dirección sede')
    usuarios_ids = fields.Many2many('res.partner', string='Usuarios')

    data_alta = fields.Date('Data de alta', default=lambda *a:datetime.now().strftime('%Y-%m-%d'))
    data_baixa = fields.Date('Data de baixa')

    estado = fields.Selection([
        ('operativo', 'Operativo'),
        ('reparandose', 'Reparandose'),
        ('reparado', 'Reparado'),
        ('baixa', 'Baixa'),
        ('irreparable', 'Irreparable')],
        'Estado', default="operativo")

    ubicacion = fields.Char('Ubicación')
    descricion = fields.Char('Descrición')
    observacions = fields.Char('Observacións')

class XestionsatComponhentesEquipo(models.Model):
    _name = 'xestionsat.componhentesequipo'
    _inherits = {'product.template': 'template_id'}
    _description = 'XestionSAT Compoñentes Equipo'

    template_id = fields.Many2one('product.template', ondelete='cascade')
    equipo_id = fields.Many2one('xestionsat.equipos', 'equipos_id', ondelete='cascade')
    nome = fields.Char('Nome descriptivo', required=True)
    observacions = fields.Char('Observacións')
