from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Avg, F, ExpressionWrapper, fields
# from .forms import ManagerSignupForm, LoginForm, OperatorSignupForm
from .forms import ManagerSignupForm, LoginForm, OperatorSignupForm, CreateQueueForm, ModifyQueueForm, ModifyOperatorForm
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
from datetime import timedelta


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



# ============= Manager =============

# Manager Dashboard
@manager_required
def manager_dashboard(request):
    manager   = Manager.objects.get(user=request.user)
    queues    = Queue.objects.filter(manager=manager)
    operators = Operator.objects.filter(manager=manager)

    for queue in queues:
        print(f"Queue: {queue.name}, Assigned Operators: {[op.user.username for op in queue.operator_set.all()]}") 

    context = {"queues"    : queues, 
               "operators" : operators,
               "manager"   : manager}
    print("-"*50)
    
    for key, value in context.items():
        print(f"Key: {key} \n {value}")
        print("-"*20)
    print("-"*50)
    
    return render(request, "manager.html", context)

# ============= Queue-Manager =============

# Create Queue
@manager_required
def create_queue(request):
    manager   = request.user.manager
    operators = Operator.objects.filter(manager=manager)

    if request.method == "POST":
        form = CreateQueueForm(request.POST, manager=manager)
        if form.is_valid():
        # Get operator info
            # List of selected operator PKs (Operator has no id as the user is its id)
            selected_operator_ids = form.cleaned_data['operators']  
            print(f"HERE selected_operator_ids: {selected_operator_ids}")

            # Fetch actual Operator objects based on their PK
            selected_operators = Operator.objects.filter(pk__in=selected_operator_ids)  
            # create a new queue object
            queue = Queue.objects.create(name=form.cleaned_data['name'],
                                         active=True,
                                         manager=manager)
            # assign operators to queues
            print(f"HERE selected_operators: {selected_operators}")
            
            queue.operator_set.set(selected_operators) 
            # Handle category creation
            categories_input = form.cleaned_data['categories']
            if categories_input:
                category_names = [name.strip() for name in categories_input.split(',')]
                for cat_name in category_names:
                    if cat_name:
                        # create a category and assign it to operator
                        Category.objects.create(name=cat_name, queue=queue)

            return redirect('manager_dashboard')
        else:
            print("HERE: form is not valid")
            print(form.errors)
    else:
        print("HERE: loading queue form")
        print(f"HERE: {manager}")
        form = CreateQueueForm(manager=manager)
    return render(request, "create_queue.html", {"form": form, "operators": operators})


@manager_required
def modify_queue(request, queue_id):
    manager = request.user.manager  # Get the logged-in manager
    queue = get_object_or_404(Queue, id=queue_id, manager=manager)  # Ensure the manager owns the queue

    if request.method == "POST":
        form = ModifyQueueForm(request.POST, instance=queue, manager=manager)
        if form.is_valid():
            # Get the updated data
            selected_operator_ids = form.cleaned_data['operators']
            selected_operators = Operator.objects.filter(pk__in=selected_operator_ids)
            print(f"HERE selected_operator_ids: {selected_operator_ids}")
            print(f"HERE selected_operators:    {selected_operators}")

            # Update queue fields
            queue.name = form.cleaned_data['name']
            queue.save()

            # Update Many-to-Many relationship
            queue.operator_set.set(selected_operators)

            # Handle categories update
            categories_input = form.cleaned_data['categories']
            queue.category_set.all().delete()  # Remove existing categories
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
        form = ModifyQueueForm(instance=queue, manager=manager)

    return render(request, 'modify_queue.html', {"form": form, "queue": queue})

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


# ============= Delete-Queue =============

@manager_required
def delete_queue_confirm(request, queue_id):
    queue = get_object_or_404(Queue, id=queue_id)
    categories = Category.objects.filter(queue=queue)

    context = { 'queue': queue,
                'categories': categories
              }
    return render(request, 'delete_queue_confirm.html', context)

@manager_required
def delete_queue(request, queue_id):
    queue = get_object_or_404(Queue, id=queue_id)

    if request.method == "POST":
        queue.delete()
        messages.success(request, f'Queue "{queue.name}" has been deleted successfully.')
        return redirect('dashboard')  # Redirect to your main dashboard or queue list page

    return redirect('delete_queue_confirm', queue_id=queue_id)


# ============= Operator-Manager =============
@manager_required
def modify_operator(request, operator_pk):
    print("HERE: modify_operator was called")
    manager = request.user.manager  # Get the logged-in manager
    operator = get_object_or_404(Operator, pk=operator_pk, manager=manager)  # Ensure the manager owns the queue

    if request.method == "POST":
        form = ModifyOperatorForm(request.POST, instance=operator, manager=manager)
        if form.is_valid():
            # Get the updated data
            selected_queue_ids = form.cleaned_data['queues']
            selected_queues = Queue.objects.filter(pk__in=selected_queue_ids)
            print(f"HERE selected_queue_ids: {selected_queue_ids}")
            print(f"HERE selected_queues:    {selected_queues}")


            # Update Many-to-Many relationship
            operator.queue.set(selected_queues)

            return redirect('manager_dashboard')
        else:
            print("HERE: form is not valid")
            print(form.errors)
    else:
        form = ModifyOperatorForm(instance=operator, manager=manager)

    return render(request, 'modify_operator.html', {"form": form, "operator": operator})





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
            return notify_guest(request)

        elif 'btnremove' in request.POST:
            return remove_guest(request)

    return render(request, 'queue_operator.html', context)

def queue_detail(request, queue_id):
    queue = Queue.objects.get(id=queue_id)
    guests = Guest.objects.filter(queue=queue).order_by('created_at')

    context = {
        "queue": queue,
        "guests": guests,
    }
    return render(request, "queue_detail.html", context)


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
        ).order_by('created_at').first()  # Get the first guest in order
        
        if guest_to_serve:
            guest_to_serve.served = True
            guest_to_serve.end_of_service_time = datetime.datetime.now()
            guest_to_serve.operator = operator 
            guest_to_serve.save()
            messages.success(request, f"Guest {guest_to_serve.name} has been served.")
        
        return redirect('operator_dashboard')  # Redirect to the dashboard after serving


# Notify a guest (send SMS)
def notify_guest(request):
    if request.method == "POST":
        queue_id = request.POST.get("queue_id")
        if not queue_id:
            return redirect('operator_dashboard')  # Safety check

        # Fetch the specific queue
        queue = Queue.objects.filter(id=queue_id).first()
        if not queue:
            return redirect('operator_dashboard')

        # Ensure guest order is based ONLY on guest_number
        guest_to_notify = Guest.objects.filter(
            queue=queue,
            served=False,
            walked_away=False,
            removed=False
        ).order_by('created_at').first()
        if guest_to_notify:
            guest_to_notify.begin_of_service_time = now()  # 
            guest_to_notify.save()

            # Send SMS alert
            send_sms(guest_to_notify.name, guest_to_notify.phone_number, request)
            print(f"Notification sent to {guest_to_notify.name} in queue {queue.name}")
        
    return redirect('operator_dashboard')

def remove_guest(request):
    # remove the guest 
    print("requestttt",request.POST)
    guest_id = request.POST.get("guest_number")
    guest_to_remove = Guest.objects.get(id=guest_id)
    guest_to_remove.removed = True
    guest_to_remove.end_of_service_time = datetime.datetime.now()  # Log the removal time
    guest_to_remove.save()
    return redirect('operator_dashboard')  # Go back to tsshe dashboard

# Twilio SMS function
def send_sms(guest_name, guest_phone,request):
    
    message_to_broadcast = f"Hello {guest_name}, it's your turn! Please proceed to the counter."

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    if guest_phone:
        client.messages.create(
            from_='whatsapp:+14155238886',  # Twilio Sandbox Number
            body=message_to_broadcast,  # Message body
            to=f'whatsapp:{guest_phone}'  # Recipient WhatsApp number
        )
        
        messages.success(request, f"Message sent successfully to {guest_name} ({guest_phone})")

def forbidden_view(request):
    return HttpResponse("Access Denied", status=403)




def queue_statistics(manager):
    """
    Generate statistics for each queue managed by the currently logged-in manager, including:
    - Most selected category
    - Average number of guests per day
    - Percentage of guests served
    - Average service time
    """
    queues = Queue.objects.filter(manager=manager)
    stats = []
    
    for queue in queues:
        guests = Guest.objects.filter(queue=queue)
        total_guests = guests.count()
        
        # Find the most selected category in the queue
        most_selected_category = (
            guests.values('category__name')
            .annotate(count=Count('category'))
            .order_by('-count')
            .first()
        )
        
        # Calculate average number of guests per day
        if total_guests > 0:
            first_guest = guests.earliest('created_at').created_at.date()
            last_guest = guests.latest('created_at').created_at.date()
            days_count = max(1, (last_guest - first_guest).days)
            avg_guests_per_day = total_guests / days_count
        else:
            avg_guests_per_day = 0
        
        # Calculate percentage of guests served
        served_guests = guests.filter(served=True).count()
        percentage_served = (served_guests / total_guests * 100) if total_guests else 0
        
        # Calculate average service time
        avg_service_time = guests.aggregate(avg_time=Avg(ExpressionWrapper(F('end_of_service_time') - F('begin_of_service_time'), output_field=fields.DurationField())))['avg_time']
        
        stats.append({
            'queue_id': queue.id,
            'queue': queue,
            'most_selected_category': most_selected_category['category__name'] if most_selected_category else 'N/A',
            'avg_guests_per_day': round(avg_guests_per_day, 2),
            'percentage_served': round(percentage_served, 2),
            'avg_service_time': avg_service_time if avg_service_time else 'N/A'
        })
    
    return stats

def operator_statistics(manager):
    """
    Generate statistics for each operator managed by the currently logged-in manager, including:
    - Average number of guests served per day
    - Average service time per guest
    - Number of queues assigned
    - The queue where they served the most guests
    - The most served category
    """
    operators = Operator.objects.filter(manager=manager)
    stats = []
    
    for operator in operators:
        guests = Guest.objects.filter(operator=operator, served=True)
        total_served = guests.count()
        
        # Calculate average guests served per day
        if total_served > 0:
            first_guest = guests.earliest('created_at').created_at.date()
            last_guest = guests.latest('created_at').created_at.date()
            days_count = max(1, (last_guest - first_guest).days)
            avg_served_per_day = total_served / days_count
        else:
            avg_served_per_day = 0
        
        # Calculate average service time per guest
        avg_service_time = guests.aggregate(avg_time=Avg(ExpressionWrapper(F('end_of_service_time') - F('begin_of_service_time'), output_field=fields.DurationField())))['avg_time']
        
        # Find the queue where the operator served the most guests
        queue_most_served = (
            guests.values('queue__name')
            .annotate(count=Count('queue'))
            .order_by('-count')
            .first()
        )
        
        # Find the most served category by the operator
        most_served_category = (
            guests.values('category__name')
            .annotate(count=Count('category'))
            .order_by('-count')
            .first()
        )
        
        stats.append({
            'operator_pk' :operator.pk,
            'operator': operator,
            'avg_served_per_day': round(avg_served_per_day, 2),
            'avg_service_time': avg_service_time if avg_service_time else 'N/A',
            'num_queues': operator.queue.count(),
            'queue_most_served': queue_most_served['queue__name'] if queue_most_served else 'N/A',
            'most_served_category': most_served_category['category__name'] if most_served_category else 'N/A'
        })
    
    return stats

def queue_operator_stats_view(request):
    """
    View to display queue and operator statistics for the currently logged-in manager.
    """
    user = request.user
    manager = Manager.objects.get(user=user)
    
    queue_stats = queue_statistics(manager)
    operator_stats = operator_statistics(manager)
    # print("-"*80)

    
    # for item in queue_stats:
    #     for key, value in item.items():
    #         print(f"Key: {key} \n\t {value}")
    #     print("-"*50)
    # print("operator")
    # for item in operator_stats:
    #     for key, value in item.items():
    #         print(f"Key: {key} \n\t {value}")
    #     print("-"*50)
    
    # print("-"*80)

    
    return render(request, 'stats.html', {'queue_stats': queue_stats, 'operator_stats': operator_stats})
