from odoo import http
from odoo.http import request

class MainController(http.Controller):

    @http.route('/reservation/create', auth='user', type='http', website=True)
    def create_reservation(self, **post):
        rooms = request.env['room.reservation'].search([])

        return request.render('nom_de_ton_module.reservation_form', {
            'rooms': rooms,
        })

    @http.route('/reservation/confirm', auth='user', type='http', website=True)
    def action_confirm_reservation(self, **post):
        # Récupère les données du formulaire
        room_name = post.get('room_name')
        date_start = post.get('date_start')
        date_end = post.get('date_end')

        # Crée une nouvelle réservation
        request.env['room.reservation'].create({
            'room_name': room_name,
            'date_start': date_start,
            'date_end': date_end,
        })
        
        # Redirige vers une page de confirmation
        return request.redirect('/reservation/success')
