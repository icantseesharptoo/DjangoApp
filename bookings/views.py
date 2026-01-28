from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Room, Booking
from django.utils import timezone

def index(request):
    rooms = Room.objects.all()
    return render(request, 'bookings/index.html', {'rooms': rooms})

from .forms import BookingForm

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    form = BookingForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.room = room
        booking.user = request.user
        
        # Simple overlap check
        overlapping_bookings = Booking.objects.filter(
            room=room,
            start_time__lt=booking.end_time,
            end_time__gt=booking.start_time
        )
        
        if overlapping_bookings.exists():
            messages.error(request, "This room is already booked for the selected time.")
        else:
            booking.save()
            messages.success(request, f"Successfully booked {room.name}!")
            return redirect('index')
            
    return render(request, 'bookings/book_room.html', {'room': room, 'form': form})

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Admin').exists())

@user_passes_test(is_admin)
def admin_dashboard(request):
    bookings = Booking.objects.all().order_by('-start_time')
    return render(request, 'bookings/admin_dashboard.html', {'bookings': bookings})

@user_passes_test(is_admin)
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.delete()
    messages.success(request, "Booking cancelled successfully.")
    return redirect('admin_dashboard')
