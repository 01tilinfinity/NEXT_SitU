from django.contrib import admin
from main.models import Reservation, Seat

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cafe', 'seat', 'reservation_time', 'number_of_people')

class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'cafe', 'seat_status', 'seats_no')

# Registering models with exception handling for already registered models
models_to_register = [
    (Reservation, ReservationAdmin),
    (Seat, SeatAdmin),
]

for model, admin_class in models_to_register:
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
