from django.shortcuts import render, redirect, get_object_or_404
from .models import ParkingSlot, Booking
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

# 1. WELCOME
def welcome(request):
    return render(request, 'parking/welcome.html')

# 2. LOGIN
def login_view(request):
    if request.method == "POST":
        u_name = request.POST.get('username')
        email = request.POST.get('email')
        p_word = request.POST.get('password')
        if u_name and email and p_word:
            return redirect('dashboard')
        else:
            messages.error(request, "Please enter Username, Email, and Password.")
    return render(request, 'parking/login.html')

# 3. DASHBOARD
def dashboard(request):
    active_bookings = Booking.objects.all()
    now = timezone.now()
    for b in active_bookings:
        end_time = b.created_at + timedelta(hours=b.duration)
        if now > end_time:
            ParkingSlot.objects.filter(slot_number=b.slot_number).update(is_occupied=False)

    v_type = request.GET.get('type')
    query = request.GET.get('q', '')
    slots = None
    if v_type:
        slots = ParkingSlot.objects.filter(slot_type=v_type).order_by('id')
        if query:
            slots = slots.filter(slot_number__icontains=query)

    available = ParkingSlot.objects.filter(is_occupied=False).count()
    reserved = ParkingSlot.objects.filter(is_occupied=True).count()
    return render(request, 'parking/dashboard.html', {
        'slots': slots, 'v_type': v_type, 'available': available, 
        'reserved': reserved, 'query': query
    })

# 4. BOOKING
def booking(request, slot_id):
    slot = get_object_or_404(ParkingSlot, id=slot_id)
    if request.method == "POST":
        v_type = request.POST.get('vehicle_type')
        duration = int(request.POST.get('duration', 1))
        rates = {'2-wheeler': 20, '3-wheeler': 30, '4-wheeler': 50}
        total = duration * rates.get(v_type, 50)
        new_booking = Booking.objects.create(
            full_name=request.POST.get('full_name'),
            vehicle_number=request.POST.get('vehicle_number'),
            vehicle_type=v_type,
            slot_number=slot.slot_number,
            duration=duration,
            total_amount=total
        )
        slot.is_occupied = True
        slot.save()
        return redirect('ticket', booking_id=new_booking.id)
    return render(request, 'parking/booking.html', {'slot': slot})

# 5. TICKET (This is the one Django was missing!)
def ticket(request, booking_id):
    booking_details = get_object_or_404(Booking, id=booking_id)
    return render(request, 'parking/ticket.html', {'booking': booking_details})