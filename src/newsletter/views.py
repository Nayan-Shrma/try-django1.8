from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm,SignUpForm
from .models import SignUp

# Create your views here.
def home(request):
    title='Sign Up Now !!'

    # print(request.user)
    # print(request.user.is_staff)
    form = SignUpForm(request.POST or None)
    # if request.user.is_authenticated():        
    #     title = "My Title %s"%(request.user)
    # if request.method == "POST":
    #   print (request.POST)

    
    
    context ={
        "title":title,
        "form":form
    }

    if (request.user.is_authenticated() and request.user.is_staff):
        # print(SignUp.objects.all())
        # i=1
        # for instance in SignUp.objects.all():
        #     print(i)
        #     print(instance.full_name)
        #     i+=1

        queryset = SignUp.objects.all().order_by("-timestamp")
        # queryset = SignUp.objects.all().order_by("-timestamp").filter(full_name__icontains="lynda")
        context = {
                "queryset": queryset
            }
    
    if form.is_valid():
        # form.save()
        #print(request.POST['email'])  #not recommended
        instance = form.save(commit=False)
        # full_name = form.clean_full_name()
        full_name = form.cleaned_data.get("full_name")
        if not full_name:
            full_name = "New Full Name"
        instance.full_name = full_name
        instance.save()
        # print(instance.email)
        # print(instance.timestamp)
        context={
            "title":"Thank You"
        }
        # print(request.user)
       
        
    
    return render(request,"home.html",context)


def contact(request):
   
    title = "Contact Us"
    form = ContactForm(request.POST or None)

    if form.is_valid():
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")

        subject = "Site contact form"
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email]
        contact_message = "%s:%s via %s"%(
            form_full_name,
            form_message,
            form_email)
        send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
        # for key,value in form.cleaned_data.items():
        #     print (key,value)
            #print(form.cleaned_data.get(key))

       # print (form.cleaned_data)
 
    context = {
        "form":form,
        "title":title,
    }
    
    return render(request,"forms.html",context)