from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ManagerSignupForm, LoginForm, OperatorSignupForm, CreateQueueForm
from .models import Manager, Operator, Queue, Category
from guests.models import Guest
from customers.decorators import manager_required, operator_required
import datetime
from django.conf import settings
from twilio.rest import Client
from django.utils.timezone import now
from django.contrib import messages
from django.shortcuts import get_object_or_404
import qrcode



def homepage(request):
    return render(request, 'index.html') 


# Manager signup view
def manager_signup(request):
    if request.method == 'POST':
        form = ManagerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = ManagerSignupForm()
    return render(request, 'signup.html', {'form': form, 'user_type': 'Manager'})

# Operator signup view
def operator_signup(request):
    if request.method == 'POST':
        form = OperatorSignupForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('manager_dashboard')
    else:
        form = OperatorSignupForm(user=request.user)
    return render(request, 'signup.html', {'form': form, 'user_type': 'Operator'})

# Login view
def user_login(request):
    
    if request.method == 'POST':
        print('HERE: method is post')
        form = LoginForm(request.POST)
        print("HERE: ", form.errors)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(f"Form is valid")
            if user:
                login(request, user)
                # Distinguish user types
                if user.is_manager:
                    # logger.info("Manager login successful for username: %s", username)
                    print("HERE: Manager login successful for username: %s", username)
                    # return HttpResponse('Hello login')
                    return redirect('manager_dashboard')  # Replace with actual URL
                elif user.is_operator:
                    # logger.info("Operator login successful for username: %s", username)
                    print("HERE: Operator login successful for username: %s", username)
                    # TODO: Redirect to operator page
                    return redirect('operator_dashboard')
                    # return redirect('operator_dashboard')
                else:
                    print(user)
            else:
                print("HERE: Login failed for username: %s", username)
                # logger.warning("Login failed for username: %s", username)
        else: 
            print("HERE: Login failed for username: ", form.cleaned_data.get('username'), "\nERROR\n",form.errors)
            # logger.warning("Login failed for username: ", form.cleaned_data.get('username'), "\nERROR\n",form.errors)

    else:
        print('HERE: login')
        
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    # logger.info("User logged out successfully")  # Log the logout event
    return redirect('login')  # Redirect to the login page after logout
# Manager Dashboard
@manager_required
def manager_dashboard(request):
    manager = Manager.objects.get(user=request.user)
    queues = Queue.objects.filter(manager=manager).prefetch_related('operator_set')
    operators = Operator.objects.filter(manager=manager)

    for queue in queues:
        print(f"Queue: {queue.name}, Assigned Operators: {[op.user.username for op in queue.operator_set.all()]}") 

    context = {"queues": queues, "operators": operators}
    return render(request, "manager.html", context)

# Create Queue
@manager_required
def create_queue(request):
    manager = request.user.manager
    operators = Operator.objects.filter(manager=manager)

    if request.method == "POST":
        form = CreateQueueForm(request.POST, manager=manager)
        if form.is_valid():
            queue = form.save(commit=False)
            queue.manager = manager  
            queue.save()
            form.save_m2m()  

            # Handle category creation
            categories_input = form.cleaned_data['categories']
            if categories_input:
                category_names = [name.strip() for name in categories_input.split(',')]
                for cat_name in category_names:
                    if cat_name:
                        Category.objects.create(name=cat_name, queue=queue)

            return redirect('manager_dashboard')
        else:
            print("HERE: form is not valid")
            print(form.errors)
    else:
        print("HERE: loading queue form")
        form = CreateQueueForm(manager=manager)
    return render(request, "create_queue.html", {"form": form, "operators": operators})


@manager_required
def generate_qr_code(request, queue_id):
    print("HERE: QR code ")
    queue = get_object_or_404(Queue, pk=queue_id)
    domain = request.get_host()

    # Generate the URL for the queue
    queue_url = f"http://{domain}/guests/enter_queue/{queue.id}"
    print(f"HERE {queue_url}")
    # Create the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(queue_url)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')

    # Return the image as an HTTP response
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


# Operator Dashboard
@operator_required
def operator_dashboard(request):
    operator = Operator.objects.get(user=request.user)
    #Get the logged-in operator
    queues = Queue.objects.filter(operator=operator)
    walked_away_guests = Guest.objects.filter(queue__in=queues, walked_away=True)
    queue_data = []
    for queue in queues:
        has_active_guests = Guest.objects.filter(
            queue=queue, served=False, walked_away=False, removed=False
        ).exists()  
    # Fetch the number of guests served by the operator
    customers_assisted = Guest.objects.filter(operator=operator, served=True).count()

    # Calculate the average service time
    served_guests = Guest.objects.filter(operator=operator, served=True, end_of_service_time__isnull=False)
    total_time = sum(
        (guest.end_of_service_time - guest.begin_of_service_time).total_seconds() / 60
        for guest in served_guests if guest.begin_of_service_time
    )
    avg_service_time = total_time / served_guests.count() if served_guests.count() > 0 else 0

    queue_data.append({
            "queue": queue,
            "has_active_guests": has_active_guests
        })
    return render(request, 'operator.html', {'operator': operator, 'queues': queues, "walked_away_guests": walked_away_guests, "queue_data": queue_data,'customers_assisted': customers_assisted,
            'avg_service_time': round(avg_service_time, 2)})

# ========== QUEUE BEHAVIOR ==========
chosenQueues = []
guestsOut = []

@operator_required
def queue_operator_view(request):
    operator = Operator.objects.get(user=request.user)
    opqueues = operator.queue.all()  # Get all queues the operator is assigned to
    context = {"opqueues": opqueues, "operator": operator}

    if request.method == 'POST':
        # if 'chooseQueue' in request.POST:
        #     return choose_queue(request, operator, context)

        if 'btnserve' in request.POST:
            return serve_guest(request, operator) 

        elif 'btnRequest' in request.POST:
            return notify_guest(request, operator)

        elif 'btnremove' in request.POST:
            return remove_guest(operator)

    return render(request, 'queue_operator.html', context)

def queue_detail(request, queue_id):
    queue = Queue.objects.get(id=queue_id)
    guests = Guest.objects.filter(queue=queue).order_by('guest_number')

    context = {
        "queue": queue,
        "guests": guests,
    }
    return render(request, "queue_detail.html", context)

# Select a queue
def choose_queue(request, operator, context):
    chosenQueue = Queue.objects.get(id=request.POST.get("queue_id"))
    chosenQueues.append(chosenQueue)

    if not chosenQueue.active:
        chosenQueue.active = True
        chosenQueue.save()

    guests = Guest.objects.filter(Q(walked_away=False) & Q(removed=False) & Q(served=False) & Q(queue=chosenQueue))
    guestNumbers = [guest.guest_number for guest in guests]

    context["guests"] = guests
    context["guestNumbers"] = min(guestNumbers) if guestNumbers else None
    return render(request, 'queue_operator.html', context)

def serve_guest(request, operator):
    if request.method == "POST":
        queue_id = request.POST.get("queue_id")  # Get queue ID from the request
        
        if not queue_id:
            return redirect('operator_dashboard')  # Ensure queue_id exists

        chosenQueue = operator.queue.filter(id=queue_id).first()  # Ensure operator is assigned to this queue
        if not chosenQueue:
            return redirect('operator_dashboard')  # Ensure queue exists and operator is assigned
        
        # Get the next guest in the queue who hasn't been served, removed, or abandoned
        guest_to_serve = Guest.objects.filter(
            queue=chosenQueue,
            served=False,
            walked_away=False,
            removed=False
        ).order_by('guest_number').first()  # Get the first guest in order
        
        if guest_to_serve:
            guest_to_serve.served = True
            guest_to_serve.end_of_service_time = datetime.datetime.now()
            guest_to_serve.operator = operator  # Assign operator serving the guest
            guest_to_serve.save()
            messages.success(request, f"Guest {guest_to_serve.name} has been served.")
        
        return redirect('operator_dashboard')  # Redirect to the dashboard after serving


# Notify a guest (send SMS)
def notify_guest(request, operator):
    if request.method == "POST":
        queue_id = request.POST.get("queue_id")  # Get queue ID from form submission
        if not queue_id:
            return redirect('operator_dashboard')  # Safety check

        # Fetch the specific queue
        queue = Queue.objects.filter(id=queue_id).first()
        if not queue:
            return redirect('operator_dashboard')  # If queue does not exist, redirect

        # Get the next guest in this queue who hasn't been served, removed, or walked away
        guest_to_notify = Guest.objects.filter(
            queue=queue,
            served=False,
            walked_away=False,
            removed=False
        ).order_by('guest_number').first()

        if guest_to_notify:
            guest_to_notify.begin_of_service_time = now()  # Mark as notified
            guest_to_notify.save()

            # Send SMS alert to the guest
            send_sms(guest_to_notify.name, guest_to_notify.phone_number)
            print(f"Notification sent to {guest_to_notify.name} in queue {queue.name}")

    return redirect('operator_dashboard')
# Remove a guest
def remove_guest(operator):
    # Find the first guest in the operator's assigned queues who has not been served, removed, or walked away
    guest_to_remove = Guest.objects.filter(
        queue__operator=operator,  # Get guests from queues assigned to this operator
        served=False,
        walked_away=False,
        removed=False
    ).order_by('guest_number').first()  # Get the first guest in line

    if guest_to_remove:
        guest_to_remove.removed = True  # Mark as removed
        guest_to_remove.end_of_service_time = datetime.datetime.now()  # Log the time
        guest_to_remove.save()

    return redirect('operator_dashboard')  # Go back to the dashboard

# Twilio SMS function
def send_sms(guest_name, guest_phone):
    
    message_to_broadcast = f"Hello {guest_name}, it's your turn! Please proceed to the counter."

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    if guest_phone:
        client.messages.create(
            from_='whatsapp:+14155238886',  # Twilio Sandbox Number
            body=message_to_broadcast,  # Message body
            to=f'whatsapp:{guest_phone}'  # Recipient WhatsApp number
        )
        messages.success(f"Message sent successfully to {guest_name} ({guest_phone}).")
