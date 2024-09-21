from odoo import models, fields,api


class Doctor (models.Model):
    _name = 'hms.doctor'
    _description = 'doctor info'
    _rec_name = 'first_name'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image=fields.Binary('file')
    patient_ids=fields.One2many('hms.patient', 'doctor_id')
    department_ids=fields.Many2many('hms.department')

    @api.onchange('department_ids')
    def _onchange_department_ids(self):
        if not self.department_ids:
            return {
                'readonly': True,
            }
        else:
            return {
                'readonly': False,
            }