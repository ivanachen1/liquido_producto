from models import intermediate
from odoo import fields, models, api
from odoo.exceptions import AccessError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    liquido_producto = fields.Boolean(string="aplicar Liquido Producto", default=False)

    intermediate_ids = fields.One2many('product.intermediateinfo', 'product_tmpl_id', string='Informacion del Intermediario')

