from django.shortcuts import render, redirect
from customers.models import Manager, Queue, Category
from guests.models import Guest
from guests.forms import GuestForm
from django.utils import timezone
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
    return render(request, "register.html", {"form": form})

def queue_guest(request, queue_id, guest_id):
    guest = Guest.objects.get(pk=guest_id)

    context = {'guest': guest}
    return render(request, "queue_dashboard.html", context)

def game(request, queue_id, guest_id):
    guest = Guest.objects.filter(id=guest_id).first()  # Simple fetch without raising an error

    context = {
        'guest': guest
    }
    return render(request, "game.html", context)