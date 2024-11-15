from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

def about(request):
    return render(request, 'about-us.html')

def contact(request):
    return render(request, 'contact-us.html')

def blogs(request):
    return render(request, 'blogs.html')
    
def custom_404_view(request):
    return render(request, 'error.html', status=404)