from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Hike, UserManager
import bcrypt
from django.db.models import Count
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw_hash)
            request.session['user_id'] = user.id
            if 'user_id' not in request.session:
                return redirect('/')
            context = {
                'current_user' : User.objects.get(id=request.session['user_id']),
                'all_hikes' : Hike.objects.all(),
            }
            return render(request, 'dashboard.html', context)
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if 'user_id'in request.session:
        context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        'all_hikes' : Hike.objects.order_by("date", "time"), #default is .objects.all() change to .objects.order_by("") to sort
        }
        return render(request, 'dashboard.html', context)
    return redirect('/')

def login(request):
    if request.method == "POST":
        registered_user = User.objects.filter(email=request.POST['email'])
        if registered_user:
            user = registered_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/dashboard')
        messages.error(request, "Incorrect email or password")
    return redirect('/')

def new(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if 'user_id'in request.session:
        context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        }
    return render(request, 'hikes/new.html', context)

def create(request):
    if request.method == "POST" and request.FILES['trailpics']:
        errors = Hike.objects.hike_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/hikes/new')
        else:
            trailpics = request.FILES['trailpics']
            fs = FileSystemStorage()
            filename = fs.save(trailpics.name, trailpics)
            url = fs.url(filename)
            one_hike = Hike.objects.create(
                title = request.POST['title'], 
                location = request.POST['location'], 
                date = request.POST['date'],
                time = request.POST['time'],
                ampm = request.POST['ampm'],
                meeting = request.POST['meeting'],
                description = request.POST['description'], 
                difficulty = request.POST['difficulty'], 
                length = request.POST['length'],
                image = url,
                creator = User.objects.get(id=request.session['user_id']))
            User.objects.get(id=request.session['user_id']).added_hikes.add(one_hike)
            return redirect('/dashboard')
    return redirect('/')

def viewhike(request, hike_id):
    context = {
        'one_hike' : Hike.objects.get(id=hike_id),
        'all_hikes' : Hike.objects.all(),
        'current_user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "hikes/hikedetails.html", context)

def delete(request, hike_id):
        delete_hike = Hike.objects.get(id=hike_id)
        delete_hike.creator.id == request.session['user_id']
        delete_hike.delete()
        return redirect('/dashboard')

def edit(request, hike_id):
    context = {
        'one_hike' : Hike.objects.get(id=hike_id),
    }
    return render(request, 'hikes/edit.html', context)

def update(request, hike_id):
    # if request.FILES['trailpics']:
        errors = Hike.objects.hike_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect((f'/hikes/{hike_id}/edit'))
        # trailpics = request.FILES['trailpics']
        # fs = FileSystemStorage()
        # filename = fs.save(trailpics.name, trailpics)
        # url = fs.url(filename)
        to_update = Hike.objects.get(id=hike_id)
        to_update.title = request.POST['title']
        to_update.location = request.POST['location']
        # to_update.date = request.POST['date']
        to_update.time = request.POST['time']
        to_update.ampm = request.POST['ampm']
        to_update.meeting = request.POST['meeting']
        to_update.description = request.POST['description']
        to_update.difficulty = request.POST['difficulty']
        to_update.length = request.POST['length']
        # to_update.image = url
        to_update.save()
        context = {
            'current_user' : User.objects.get(id=request.session['user_id']),
            'all_hikes' : Hike.objects.order_by("date", "time"),
            }
        return render(request, 'dashboard.html', context)

def join(request, hike_id):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session['user_id'])
    one_hike = Hike.objects.get(id=hike_id)
    current_user.added_hikes.add(one_hike)
    return redirect('/dashboard')

def notjoin(request, hike_id):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session["user_id"])
    one_hike = Hike.objects.get(id=hike_id)
    current_user.added_hikes.remove(one_hike)
    return redirect('/dashboard')
