from odoo import fields, models, api
from odoo.exceptions import ValidationError


class task(models.Model):
    _name = "manage.task"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Task manager"
    _rec_name = "task_name"

    task_id = fields.Char(string="Task Id")
    task_name = fields.Char(string="Task to do", tracking=True, copy=False, help="Assign a work to do",required=True)
    employee_id = fields.Integer(string="Employee_id", tracking=True, default='')
    assign_id = fields.Many2one("res.users", string="Assign To", tracking=True)
    deadline = fields.Date(string='Deadline', tracking=True)
    balance_days = fields.Integer(string='Days To Complete', compute='_compute_balance_days')
    remark = fields.Html(string='Remark')
    image = fields.Image(string="Image")
    skillsets = fields.Many2many("skillslist.task", string="Skillsets")
    email = fields.Char(string="Email")
    task_status = fields.Selection([
        ('normal', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='', string='Task status')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], default='medium', string='Priority')
    star = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Star")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('delivered', 'Delivered')], default="draft", string="state", required=True)


    @api.depends('deadline')
    def _compute_balance_days(self):
        today = fields.Date.today()

        for tasks in self:
            if tasks.deadline:
                deadline_date = fields.Date.from_string(tasks.deadline)
                remaining_days = (deadline_date - today).days
                tasks.balance_days = remaining_days
            else:
                tasks.balance_days = 0

    @api.model
    def create(self, vals):
        vals['task_id'] = self.env['ir.sequence'].next_by_code('manage.task')
        return super(task, self).create(vals)

    # @api.constrains('deadline')
    # def check_deadline(self):
    #     for rec in self:
    #         if rec.deadline and rec.deadline < rec.Date.today():
    #             raise ValidationError(_("Select date in future"))

    def object_button(self):
        print("button clicked......")
        for rec in self:
            rec.state = 'draft'
        return {
            'effect': {
                'fadeout': 'fast',
                'message': 'Submitted Successfully',
                'type': 'rainbow_man',
            }
        }

    def action_assign(self):
        for rec in self:
            rec.state = 'assigned'

    def action_delivered(self):
        for rec in self:
            rec.state = 'delivered'

    def send_emails(self):
        template_id = self.env.ref('task_management.student_card_email_template').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
