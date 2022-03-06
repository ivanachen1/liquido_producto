from odoo import fields, models, api
from odoo.exceptions import AccessError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    liquido_producto = fields.Boolean(string="aplicar Liquido Producto", default=False)

