from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class Patient (models.Model):
    _name = 'hms.patient'
    _description = 'Patient info '
    _rec_name = 'first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()
    history=fields.Html()
    cr_ratio=fields.Float()
    blood_type=fields.Selection(
        [
            ('A+', 'A+'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B-', 'B-'),
            ('O+', 'O+'),
            ('O-', 'O-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-'),
        ]
    )
    pcr=fields.Boolean(compute='_compute_pcr',readonly=False)
    image = fields.Binary('File')
    email=fields.Char()
    address = fields.Char()
    age = fields.Integer(compute='_compute_age',store=True)
    department_id = fields.Many2one('hms.department')
    doctor_id = fields.Many2one('hms.doctor')
    department_capacity = fields.Integer(related='department_id.capacity')
    patient_log_ids=fields.One2many('hms.patient.log','patient_id')
    state = fields.Selection([('Undetermined', 'Undetermined'),('Good','Good'),('Fair','Fair'),('Serious','Serious')],default='Undetermined')
    related_partner_id = fields.One2many('res.partner', 'related_patient_id')


    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age = relativedelta(fields.Date.today(), rec.birth_date).years
            else:
                rec.age = 0
    @api.depends('birth_date')
    def _compute_pcr(self):
        for rec in self:
            if rec.age < 30 and not rec.pcr and rec.age !=0:
                rec.pcr = True

    @api.constrains('department_id')
    def _check_department_id(self):
        for rec in self:
            if rec.department_id and not rec.department_id.is_opened:
                raise ValidationError('cannot assign patient to closed department')

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email:
                if '@' not in rec.email or '.' not in rec.email.split('@')[-1]:
                    raise ValidationError('invalid email format')
                existing_email=self.search([('email','=',rec.email)])
                if existing_email and existing_email.id !=rec.id:
                    raise ValidationError('email already registered')

    def write(self, vals):
        res = super(Patient, self).write(vals)
        for rec in self:
            if 'state' in vals:
                    self.env['hms.patient.log'].create({
                        'patient_id': rec.id,
                        'created_by': self.env.user.id,
                        'description': f'State changed to {vals["state"]}',
                        'date': fields.Date.today(),
                    })
        return res

    @api.constrains('pcr','cr_ratio')
    def _check_pcr(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError('Cr Ratio field is mandatory cause Pcr is checked')

    _sql_constraints = [
        ('pcr_check',
         'CHECK((pcr = TRUE))',
         'Cr Ratio field is mandatory when PCR is checked.')
    ]
    def action_undetermined(self):
        self.state = 'Undetermined'
    def action_good(self):
        self.state = 'Good'
    def action_fair(self):
        self.state = 'Fair'
    def action_serious(self):
        self.state = 'Serious'
class PatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'

    patient_id = fields.Many2one('hms.patient')
    created_by=fields.Many2one('res.users')
    description=fields.Char()
    date=fields.Date()
