from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from qindari import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to Qindari!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Qindari!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Qindari!!"
        message2 = render_to_string('authentication/registration_confirmation_email.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        #email.fail_silently = True
        print(message2)
        print("Sending confirmation email")
        email.send()
        
        return render(request, "authentication/signup_accepted.html")
        
        
    return render(request, "authentication/signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return redirect('dashboard')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')
    
    return render(request, "authentication/signin.html")

@login_required
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return render(request, 'authentication/signout_done.html')


def password_change_request(request):
    print("In password_change_request xxxx")
    if request.method == "POST":
        email_address = request.POST['email_address']
        if User.objects.filter(email=email_address).exists():
            myuser = User.objects.get(email=email_address)
            # Create password reset email 
            current_site = get_current_site(request)
            email_subject = "Qindari assword reset confirmation"
            message = render_to_string('authentication/password_reset_email.html',{
                
                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
            )
            email.fail_silently = True
            email.send()
            
        return render(request, 'authentication/password_change_done.html')

    return render(request, "authentication/password_change_request.html")
        

def password_change_done(request):
    print("In password_reset_email_sent")
    render(request, "password_reset_email_sent.html")

def password_reset_request(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None
        messages.success(request, "Error: Your password has not changed!!")
        return redirect('home')
    if request.method == "POST":
        password = request.POST['password']
        myuser.set_password(password)
        myuser.save()
        messages.success(request, "Your password has been successfully changed!!")
        return render(request, 'authentication/password_reset_done.html')
    else:
        context = {
            'uidb64': uidb64,
            'token': token
        }
        return render(request, 'authentication/password_reset_request.html', context)




def password_reset_done(request):
    print("In password_reset_done")
