from odoo import api, fields, models
from . import food_order_items


class Order(models.Model):
    _name = "food.order"
    _description = "Food Order"

    STATE_SELECTION = [
        ("draft", "Draft"),
        ("submit", "Submitted"),
        ("in_transit", "In Transit"),
        ("delivered", "Delivered"),
        ("cancel", "Cancelled"),
    ]

    customer_name = fields.Char("Customer", required=True)
    delivery_date = fields.Datetime("Delivery Date", required=True)
    address = fields.Text("Address", required=True)
    contact_no = fields.Char("Contact No.", required=True)
    amount = fields.Float("Amount", required=True, compute="_compute_amount")
    delivery_fee = fields.Float("Delivery Fee", required=True)
    total_amount = fields.Float("Total Amount", required=True)
    reward_points = fields.Float(
        "Reward Points", required=True, compute="_compute_rewards"
    )

    order_ids = fields.One2many("food.order.items", "order_id", "Food Items")

    state = fields.Selection(STATE_SELECTION, string="Status", default="draft")

    @api.depends("total_amount")
    def _compute_rewards(self):
        self.reward_points = self.total_amount / 200

    @api.depends("order_ids", "delivery_fee")
    def _compute_amount(self):
        for i in self:
            if i.delivery_fee < 1:
                i.delivery_fee = 0
            amount = 0
            for order in i.order_ids:
                amount += order.amount
            i.amount = amount
            i.total_amount = i.amount + i.delivery_fee

    def submit(self):
        self.state = "submit"

    def in_transit(self):
        self.state = "in_transit"

    def delivered(self):
        self.state = "delivered"

    def cancel(self):
        self.state = "cancel"

    def draft(self):
        self.state = "draft"
