from django.shortcuts import render, redirect, HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import ManagerSignupForm, LoginForm, OperatorSignupForm, CreateQueueForm
from .models import Manager, Operator, Queue, Category
# from .forms import ManagerSignupForm, OperatorSignupForm, CustomerSignupForm, LoginForm
from customers.decorators import manager_required, operator_required

# Manager signup view
def manager_signup(request):
    if request.method == 'POST':
        form = ManagerSignupForm(request.POST)
        print("Request is post")

        if form.is_valid():
            form.save()
           
            print("Sign up succeeded")
            return redirect('login')
            # return HttpResponse("Hello man")
        else:
            print("HERE:")
            print(form.errors)
    else:
        print("HERE:")

        form = ManagerSignupForm()
    return render(request, 'signup.html', {'form': form, 'user_type': 'Manager'})

# Operator signup view
def operator_signup(request):
    print("operator signup")
    if request.method == 'POST':
        form = OperatorSignupForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            print("Sign up succeeded")
            return redirect('manager_dashboard')
    else:
        form = OperatorSignupForm(user=request.user)
        print("Sign up operator page loaded")

    return render(request, 'signup.html', {'form': form, 'user_type': 'Operator'})




# import logging
# logger = logging.getLogger('myapp')


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


@manager_required
def manager_dashboard(request):
    manager   = Manager.objects.get(user=request.user)
    print(manager)
    print(type(manager))
    queues    = Queue.objects.filter(manager=manager)
    operators = Operator.objects.filter(manager=manager)


    context  = {"queues" : queues,
                "operators" : operators,}
    
    return render(request, 'manager.html', context)


from django.shortcuts import render, redirect
from .models import Queue, Category, Operator
from .forms import CreateQueueForm

@manager_required
def create_queue(request):
    manager = getattr(request.user, 'manager', None)  
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

            return redirect('dashboard')  
        else:
            print("HERE: form is not valid")
            print(form.errors)
    else:
        print("HERE: loading queue form")
        form = CreateQueueForm(manager=manager)

    return render(request, "create_queue.html", {"form": form, "operators": operators})



@operator_required
def operator_dashboard(request):
    # manager   = Manager.objects.get(user=request.user)
    # print(manager)
    # print(type(manager))
    # queues    = Queue.objects.filter(manager=manager)
    # operators = Operator.objects.filter(manager=manager)


    # context  = {"queues" : queues,
    #             "operators" : operators,}
    
    return render(request, 'operator.html', {})
