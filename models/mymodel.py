from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RoomReservation(models.Model):
    _name = 'room.reservation'
    _description = 'Réservation de salles'

    room_name = fields.Char(string='Nom de la salle', required=True)
    date_start = fields.Datetime(string='Date de début', required=True)
    date_end = fields.Datetime(string='Date de fin', required=True)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start >= record.date_end:
                raise ValidationError("La date de début doit être avant la date de fin.")

    @api.constrains('room_name', 'date_start', 'date_end')
    def _check_room_availability(self):
        for record in self:
            domain = [
                ('room_name', '=', record.room_name),
                '|',
                    ('date_start','<', record.date_end),
                    ('date_end', '>', record.date_start),
            ]
            conflicting_reservations = self.search(domain)
            if conflicting_reservations:
                raise ValidationError("La salle est déjà réservée pendant cette période.")

