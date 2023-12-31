from django.shortcuts import render
from .forms import UserForm, ProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Create your views here.
import sys



def accueil(request):
    return render(request, 'utilisateurs/index.html')


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)   
       ## profile_form = ProfileForm(data=request.POST)
        if user_form.is_valid(): ## and profile_form.is_valid():
            user = user_form.save()
            user.save()
         ##   profile = profile_form.save(commit=False)
           ## profile.user = user
            ##profile.save()
            registered=True
            return HttpResponseRedirect('login')        

        else:
            print(user_form.errors)

    else:
        user_form=UserForm()
        ## profile_form = ProfileForm()

    content ={
        'registered':registered,
        'form':user_form,
        ##'form2':profile_form,
    }
    return render(request, 'utilisateurs/register.html', content)        
            
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("L'utilisateur es desactive")
        else:
            return HttpResponse("Soit votre nom ou votre password est incorrect") 
    else:
        return render(request, 'utilisateurs/login.html') 


def apropos(request):
    return render(request, 'utilisateurs/apropos.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def myprofil(request):
    user = request.user
    return render(request, 'utilisateurs/myprofil.html', {'user': user})

#def bibliotheques(request):
#    return render(request, 'utilisateurs/bibliotheques.html')



