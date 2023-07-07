from odoo import api, fields, models


class FoodOrderItems(models.Model):
    _name = "food.order.items"
    _description = "Food Order Items"

    order_id = fields.Many2one("food.order", "Order")
    item_id = fields.Many2one(
        "product.product",
        "Food Item",
        domain="[('categ_id', '=', 'Food')]",
        default="product.product[0]",
    )
    price = fields.Float("Price")
    quantity = fields.Integer("Quantity")
    amount = fields.Float("Amount")

    @api.onchange("item_id")
    def onchange_item_id(self):
        if self.item_id:
            self.price = self.item_id.lst_price
            self.quantity = 1
            self.amount = self.quantity * self.price

    @api.onchange("quantity")
    def onchange_quantity(self):
        if self.quantity > 1:
            self.amount = self.quantity * self.price
        else:
            self.quantity = 1
            self.amount = self.quantity * self.price
