from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceProvider, Service, Booking, User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from .models import Review
from django.db.models import Avg
from django.core.management import call_command
from django.http import HttpResponse

def run_migrate(request):
    try:
        call_command('makemigrations')
        call_command('migrate')
        return HttpResponse("Migrations ran successfully.")
    except Exception as e:
        return HttpResponse(f"Migration failed: {str(e)}")


def leave_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    user_id = request.session.get('user_id')
    if not user_id or booking.user.id != user_id:
        return redirect('login')

    if request.method == 'POST':
        rating = int(request.POST['rating'])
        comment = request.POST['comment']
        Review.objects.create(
            booking=booking,
            rating=rating,
            comment=comment
        )

        # Update average rating
        provider = booking.provider
        avg_rating = Review.objects.filter(booking__provider=provider).aggregate(Avg('rating'))['rating__avg']
        provider.rating = round(avg_rating or 0, 1)
        provider.save()

        return redirect('my_bookings')

    return render(request, 'review.html', {'booking': booking})

def my_bookings(request):
    uid = request.session.get('user_id')
    if not uid:
        return redirect('login')

    bookings = (
        Booking.objects
        .filter(user_id=uid)
        .select_related('provider', 'service')
        .prefetch_related(
            Prefetch('review_set',
                     queryset=Review.objects.all(),
                     to_attr='reviews')
        )
    )
    print("DEBUG: Found bookings for user", uid, "→", list(bookings))  # << add this
    return render(request, 'my_bookings.html', {'bookings': bookings})


from django.db.models import Prefetch
from .models import Review
def provider_reviews(request, provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    reviews = Review.objects.filter(booking__provider=provider).select_related('booking__user')
    return render(request, 'provider_reviews.html', {'provider': provider, 'reviews': reviews})


def leave_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Make sure the user owns this booking
    user_id = request.session.get('user_id')
    if not user_id or booking.user.id != user_id:
        return redirect('login')

    if request.method == 'POST':
        rating = int(request.POST['rating'])
        comment = request.POST['comment']
        Review.objects.create(
            booking=booking,
            rating=rating,
            comment=comment
        )
        return redirect('my_bookings')

    return render(request, 'review.html', {'booking': booking})


@csrf_exempt
def update_status(request, booking_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        booking = Booking.objects.get(id=booking_id)
        booking.status = new_status
        booking.save()
    return redirect('view_bookings')


def home(request):
    providers = None
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        location     = request.POST.get('location')
        providers = ServiceProvider.objects.filter(
            service_type__icontains=service_type,
            location__icontains=location
        )
    return render(request, 'home.html', {'providers': providers})


def book_provider(request, provider_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    provider = get_object_or_404(ServiceProvider, id=provider_id)
    services = Service.objects.all()

    if request.method == 'POST':
        # Get logged-in user
        user_obj = User.objects.get(id=user_id)

        # Optional: update their profile from form
        user_obj.name = request.POST['name']
        user_obj.email = request.POST['email']
        user_obj.phone = request.POST['phone']
        user_obj.address = request.POST['address']
        user_obj.save()

        # Create booking
        service_id = request.POST['service']
        booking_date = request.POST['booking_date']
        booking_time = request.POST['booking_time']
        service = get_object_or_404(Service, id=service_id)

        Booking.objects.create(
            user=user_obj,
            provider=provider,
            service=service,
            booking_date=booking_date,
            booking_time=booking_time,
            status='Pending',
        )
        return redirect('booking_success')

    return render(request, 'book.html', {
        'provider': provider,
        'services': services
    })


def booking_success(request):
    return render(request, 'success.html')
def view_bookings(request):
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = Booking.objects.filter(status=status_filter)
    else:
        bookings = Booking.objects.all()

    bookings = bookings.select_related('user', 'provider', 'service')
    return render(request, 'bookings.html', {
        'bookings': bookings,
        'status_filter': status_filter
    })
from django.shortcuts import render, redirect
from .models import User, Booking

def signup(request):
    if request.method == 'POST':
        name    = request.POST['name']
        email   = request.POST['email']
        phone   = request.POST['phone']
        address = request.POST['address']
        pw      = request.POST['password']
        pw2     = request.POST['confirm_password']
        if pw != pw2:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered.'})
        user = User.objects.create(name=name, email=email, phone=phone, password=pw, address=address)
        request.session['user_id'] = user.id
        return redirect('home')
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        pw    = request.POST['password']
        user  = User.objects.filter(email=email, password=pw).first()
        if not user:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
        request.session['user_id'] = user.id
        return redirect('home')
    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('home')



def my_bookings(request):
    uid = request.session.get('user_id')
    if not uid:
        return redirect('login')

    # Prefetch reviews related to each booking
    bookings = (
        Booking.objects
        .filter(user_id=uid)
        .select_related('provider', 'service')
        .prefetch_related(
            Prefetch('review_set',
                     queryset=Review.objects.all(),
                     to_attr='reviews')  # each booking.reviews will be a list
        )
    )
    return render(request, 'my_bookings.html', {'bookings': bookings})
def provider_reviews(request, provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    reviews  = Review.objects.filter(booking__provider=provider).select_related('booking__user')
    return render(request, 'provider_reviews.html', {
        'provider': provider,
        'reviews':  reviews
    })
