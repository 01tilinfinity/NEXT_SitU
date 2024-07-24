from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from main.models import Seat, Reservation  # main 앱에서 모델을 가져옴
from django.contrib.auth.decorators import login_required
from accounts.models import Cafe

@login_required
def seat_overview(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    seats = Seat.objects.filter(cafe=cafe)
    reservations = Reservation.objects.filter(cafe=cafe)

    context = {
        'cafe': cafe,
        'seats': seats,
        'reservations': reservations,
    }

    return render(request, 'reservations/seat_overview.html', context)


@login_required
def update_seat_status(request, cafe_id, seat_id, status):
    seat = get_object_or_404(Seat, id=seat_id)
    if status == 'occupied':
        seat.seat_status = 'occupied'
        seat.seat_start_time = timezone.now()
    elif status == 'reserved':
        seat.seat_status = 'reserved'
    elif status == 'available':
        seat.seat_status = 'available'
        seat.seat_start_time = None
    
    seat.save()

    reservations = Reservation.objects.filter(seat=seat)
    for reservation in reservations:
        if status == 'available':
            reservation.delete() 
        else:
            reservation.seat.seat_status = status
            reservation.save()

    return redirect('seat_overview', cafe_id=cafe_id)

@login_required
def confirm_reservation(request, cafe_id, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    seat = reservation.seat
    seat.seat_status = 'reserved'
    seat.save()
    reservation.seat = seat
    reservation.save()
    return redirect('seat_overview', cafe_id=cafe_id)

@login_required
def cancel_reservation(request, reservation_id, seat_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, seat__id=seat_id)
    seat = reservation.seat
    seat.seat_status = 'available'
    reservation.delete()
    seat.save()
    
    return redirect('seat_overview', cafe_id=seat.cafe.id)

@login_required
def seat_check(request, cafe_id, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)
    if seat.seat_status == 'reserved':
        seat.seat_status = 'occupied'
        seat.seat_start_time = timezone.now()
    seat.save()
    return redirect('seat_overview', cafe_id=cafe_id)

@login_required
def create_reservation(request, cafe_id, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)
    reservation = Reservation.objects.create(seat=seat, cafe=seat.cafe, user_id=request.user.id)
    seat.seat_status = 'requesting'
    seat.save()
    return redirect('seat_overview', cafe_id=cafe_id)
