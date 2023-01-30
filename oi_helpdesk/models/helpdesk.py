from odoo import api, fields, models, tools, _
from datetime import datetime, date, timedelta


TICKET_PRIORITY = [
    ('0', 'All'),
    ('1', 'Low priority'),
    ('2', 'High priority'),
    ('3', 'Urgent'),
]

class HelpdeskInherit(models.Model):
    _inherit = "helpdesk.ticket"


    def _default_team_id(self):
        
        return 

    due_date = fields.Datetime(string="Due Date", copy=False, tracking=True)
    date_start = fields.Datetime(string="Start Date", copy=False ,tracking=True)
    end_date = fields.Date(string="End Date", copy=False, tracking=True)
    planned_hours = fields.Char(string="Planned Hours", copy=False, tracking=True)
    actual_hours = fields.Float(string="Actual Hours", copy=False, tracking=True)
    actual_complete_date = fields.Datetime(string="Actual Complete Date",copy=False, tracking=True)
    difference_date = fields.Float(string="Difference Date",compute="_compute_difference_date",store=True, copy=False, tracking=True)
    remarks = fields.Text(string="Remarks", copy=False, tracking=True)

    name = fields.Char(string='Subject', required=True, index=True, tracking=True)
    team_id = fields.Many2one('helpdesk.team', string='Helpdesk Team', default=_default_team_id,index=True, tracking=True)
    ticket_type_id = fields.Many2one('helpdesk.ticket.type', string="Type", tracking=True)
    priority = fields.Selection(TICKET_PRIORITY, string='Priority', default='0', tracking=True)
    tag_ids = fields.Many2many('helpdesk.tag', string='Tags')
    company_id = fields.Many2one(related='team_id.company_id', string='Company', store=True, readonly=True, tracking=True)
    partner_email = fields.Char(string='Customer Email', compute='_compute_partner_email', store=True, readonly=False, tracking=True)
    partner_phone = fields.Char(string='Customer Phone', compute='_compute_partner_phone', store=True, readonly=False, tracking=True)





    @api.depends('due_date', 'actual_complete_date')
    def _compute_difference_date(self):
        for record in self:
            record.difference_date = 0
            if record.due_date and record.actual_complete_date:
                
                record.difference_date = (record.due_date - record.actual_complete_date).days 

    @api.depends('partner_id')
    def _compute_partner_email(self):
        for ticket in self:
            if ticket.partner_id:
                ticket.partner_email = ticket.partner_id.email    

    @api.depends('partner_id')
    def _compute_partner_phone(self):
        for ticket in self:
            if ticket.partner_id:
                ticket.partner_phone = ticket.partner_id.phone 
                

    # @api.depends('due_date', 'date_start', 'end_date')
    # def _compute_date(self):    
    #     for record in self:
    #         if record['due_date']:
    #             record['end_date'] = record['date_start'] + datetime.timedelta(days=record['number_of_days']) 


    