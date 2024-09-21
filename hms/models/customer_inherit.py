from odoo import models,fields,api
from odoo.api import constrains
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    related_patient_id = fields.Many2one('hms.patient')

    @api.constrains('email')
    def _check_email_not_in_patients(self):
        for rec in self:
            if rec.email:
                existing_email=self.env['hms.patient'].search([('email', '=', rec.email)])
                if existing_email:
                    raise ValidationError(f'the email {rec.email} already exists in patients model')

    def unlink(self):
        for res in self:
            if res.related_patient_id:
                raise ValidationError ("You cannot delete a customer that is linked to a patient.")
        return super(ResPartner, self).unlink()

