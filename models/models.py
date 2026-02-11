from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EmployeeReward(models.Model):
    _name = 'employee.reward'  # Nom technique du modèle
    _description = 'Récompense pour un employé'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Titre de la récompense', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employé', required=True)
    reward_type = fields.Selection([
        ('bonus', 'Bonus'),
        ('recognition', 'Reconnaissance'),
        ('points', 'Points')
    ], string='Type de récompense', default='recognition')
    points = fields.Integer(string='Points', default=0)
    date_reward = fields.Date(string='Date de la récompense', default=fields.Date.today)
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmée'),
        ('approved', 'Approuvée'),
        ('done', 'Attribuée'),
        ('cancel', 'Annulée'),
    ], default='draft', tracking=True)
    reward_count = fields.Integer(
        compute='_compute_reward_count',
        string="Nombre de récompenses"
    )

    def generate_zpl(self):
        """
        Génère un ZPL pour l'impression d'une étiquette de récompense.
        """
        self.ensure_one()
        zpl = f"""
        ^XA
        ^FO50,50^A0N,30,30^FDRécompense: {self.name}^FS
        ^FO50,90^A0N,25,25^FDEmployé: {self.employee_id.name}^FS
        ^FO50,130^A0N,25,25^FDPoints: {self.points}^FS
        ^FO50,170^A0N,25,25^FDDate: {self.date_reward}^FS
        ^XZ
        """
        return zpl


    def action_print_zpl(self):
        zpl_code = self.generate_zpl()
        # Pour l'instant on le renvoie pour debug
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': "ZPL généré",
                'message': zpl_code,
                'type': 'info',
                'sticky': False
            }
        }
 
    def action_print_pdf(self):
        self.ensure_one()
        report = self.env['ir.actions.report']._get_report_from_name('employee_rewards.employee_reward_report_action')
        return report.report_action(self)



    # Calculer automatiquement les points si c’est un bonus
    @api.onchange('reward_type')
    def _onchange_reward_type(self):
        if self.reward_type == 'bonus':
            self.points = 100
        elif self.reward_type == 'recognition':
            self.points = 50
        else:
            self.points = 0

    @api.depends('employee_id')
    def _compute_reward_count(self):
        for rec in self:
            rec.reward_count = self.search_count([
                ('employee_id', '=', rec.employee_id.id)
            ])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nouveau') == 'Nouveau':
                vals['name'] = self.env['ir.sequence'].next_by_code('employee.reward')
        return super().create(vals_list)
    
    @api.constrains('employee_id', 'date_reward')
    def _check_unique_reward(self):
        for rec in self:
            count = self.search_count([
                ('employee_id', '=', rec.employee_id.id),
                ('date_reward', '=', rec.date_reward),
                ('id', '!=', rec.id)
            ])
            if count:
                raise ValidationError(
                    "Une récompense existe déjà pour cet employé à cette date."
                )


    def action_view_employee_rewards(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Récompenses',
            'res_model': 'employee.reward',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.employee_id.id)],
        }
    
    def action_confirm(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError("Seuls les brouillons peuvent être confirmés.")
            rec.state = 'confirmed'

    def action_approve(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise ValidationError("Seules les récompenses confirmées peuvent être approuvées.")
            rec.state = 'approved'

    def action_done(self):
        for rec in self:
            if rec.state != 'approved':
                raise ValidationError("Seules les récompenses approuvées peuvent être attribuées.")
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError("Impossible d’annuler une récompense déjà attribuée.")
            rec.state = 'cancel'




