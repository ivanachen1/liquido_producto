import logging
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


from odoo.tools import float_compare, float_round


class IntermediateInfo(models.Model):
    _name = "product.intermediateinfo"
    _description = "Intermediate Pricelist"
    _order = 'sequence, min_qty DESC, price, id'

    name = fields.Many2one(
        'res.partner', 'Intermediate',
        ondelete='cascade', required=True,
        help="Intermediate of this product", check_company=True)
    product_name = fields.Char(
        'intermediate Product Name',
        help="This intermediate's product name will be used when printing a request for quotation. Keep empty to use the internal one.")
    product_code = fields.Char(
        'intermediate Product Code',
        help="This intermediate's product code will be used when printing a request for quotation. Keep empty to use the internal one.")
    sequence = fields.Integer(
        'Sequence', default=1, help="Assigns the priority to the list of product intermediate.")
    product_uom = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        related='product_tmpl_id.uom_po_id',
        help="This comes from the product form.")
    min_qty = fields.Float(
        'Quantity', default=0.0, required=True, digits="Product Unit Of Measure",
        help="The quantity to purchase from this intermediate to benefit from the price, expressed in the intermediate Product Unit of Measure if not any, in the default unit of measure of the product otherwise.")
    price = fields.Float(
        'Price', default=0.0, digits='Product Price',
        required=True, help="The price to purchase a product")
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.company.id, index=1)
    currency_id = fields.Many2one(
        'res.currency', 'Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True)
    date_start = fields.Date('Start Date', help="Start date for this intermediate price")
    date_end = fields.Date('End Date', help="End date for this intermediate price")
    product_id = fields.Many2one(
        'product.product', 'Product Variant', check_company=True,
        help="If not set, the intermediate price will apply to all variants of this product.")
    product_tmpl_id = fields.Many2one(
        'product.template', 'Product Template', check_company=True,
        index=True, ondelete='cascade')
    product_variant_count = fields.Integer('Variant Count', related='product_tmpl_id.product_variant_count')
    delay = fields.Integer(
        'Delivery Lead Time', default=1, required=True,
        help="Lead time in days between the confirmation of the purchase order and the receipt of the products in your warehouse. Used by the scheduler for automatic computation of the purchase order planning.")
