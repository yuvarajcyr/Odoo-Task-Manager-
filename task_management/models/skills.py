from odoo import fields, models


class skill(models.Model):
    _name = "skillslist.task"
    _description = "Skillset List"
    _rec_name = "skill"

    skill = fields.Char(string="skill")
    color = fields.Integer(string="color")
