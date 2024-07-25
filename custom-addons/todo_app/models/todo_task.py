from odoo import models, fields

class TodoTask(models.Model):
    _name = 'todo.task'

    name = fields.Char('Task Name')
    due_date = fields.Date()
    description = fields.Text()
    assign_to_id = fields.Many2one('res.partner')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progrees'),
        ('completed', 'Completed'),
    ])
