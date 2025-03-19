from django.shortcuts import render, redirect
from customers.models import Manager, Queue, Category
from guests.models import Guest
from guests.forms import GuestForm
from django.utils import timezone
from django.http import JsonResponse

# Create your views here.

def guest_page(request, queue_id):
    queue      = Queue.objects.get(pk=queue_id)
    manager    = Manager.objects.get(pk=queue.manager)
    customer   = manager.customer
    categories = Category.objects.filter(queue=queue)

    if request.method == 'POST':
        form = GuestForm(request.POST, categories=categories)

        if form.is_valid():
            print("HERE: Form valid")

            # Get the Location object directly from the form
            chosen_category = form.cleaned_data['category']  # This is now a Location object
            # Create a vehicle object
            new_guest = Guest.objects.create(
                name         = form.cleaned_data.get("name"),
                phone_number = form.cleaned_data.get('phone_number'),
                category     = chosen_category,              # This is now the Location object
                queue        = queue,                       # Associate with the queue passed in the form
                manager      = manager,
                customer     = customer,
                created_at   = timezone.now())
            
            new_guest.save()
            guest_id=new_guest.id 
            return redirect("queue_guest", queue_id= queue.id ,guest_id=guest_id )
        else:
            print("Form errors: ", form.errors)
    else:
        print("HERE: form loading")
        form = GuestForm(categories=categories)
        print(f"HERE: \n{form}")

    context = {'form': form}
    show_popup = False
    return render(request, "register.html", {"form": form, 'show_popup': show_popup })

def queue_guest(request, queue_id, guest_id):
    guest = Guest.objects.get(pk=guest_id)
    
    context = {'guest': guest, 'walked_away': guest.walked_away, 'removed':guest.removed }
    return render(request, "queue_dashboard.html", context)

def game(request, queue_id, guest_id):
    guest = Guest.objects.filter(id=guest_id).first()  # Simple fetch without raising an error
    show_popup = False
    context = {
        'guest': guest,
        'show_popup': show_popup 
    }
    return render(request, "game.html", context)

    
from django.http import JsonResponse

def refresh_queue_status(request, guest_id):
    guest = Guest.objects.get(id=guest_id)
    queue = guest.queue
    print(f"View Called: Method = {request.method}") 
    if guest.walked_away:
        return JsonResponse({
            "status": "walked_away",
            "message": f"{guest.name} has walked away."
        })
    guests_ahead = Guest.objects.filter(
        queue=queue, 
        served=False, 
        walked_away=False, 
        removed=False, 
        guest_number__lt=guest.guest_number if guest.guest_number else 0
    ).count()

    estimated_wait_time = guests_ahead * 5  

    # Return JSON response instead of reloading the page
    return JsonResponse({
        "guest_name": guest.name,
        "queue_name": guest.queue.name,
        "guests_ahead": guests_ahead,
        "estimated_wait_time": estimated_wait_time
    })
    
def walk_away(request, guest_id):
    guest = Guest.objects.get(pk=guest_id)
    guest.walked_away = True  # Update status
    guest.save()

    return JsonResponse({"status": "success", "message": f"{guest.name} has walked away!"})

