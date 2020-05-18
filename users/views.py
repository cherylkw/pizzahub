from django.shortcuts import render, redirect
from django.contrib import messages
from .form import RegisterForm, RegisterUpdateForm
from django.contrib.auth.decorators import login_required
from orders.views import Category


# Create your views here.

# register a new user
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can log in now.')
            return redirect('login')
    else:
        form = RegisterForm()
    context = {
        'form': form,
        'title': 'Create an account',
        "Category": Category.objects.all()
    }
    return render(request, 'users/register.html', context)




'''
messages.debug
messages.info
messages.success
messages.warning
meassages.error
'''