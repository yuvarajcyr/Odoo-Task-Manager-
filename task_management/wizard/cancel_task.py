from odoo import fields, models


class cancel(models.Model):
    _name = "cancel.task"
    _description = "Cancel task"
    _rec_name = ""

    cancel = fields.Many2one("manage.task", string="Cancel")

    def action_cancel(self):
        pass

