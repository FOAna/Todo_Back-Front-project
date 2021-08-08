from django.http import HttpResponse, HttpResponseRedirect
from .models import Todo, Pomodoro
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, LoginForm
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.http import HttpResponseNotFound


def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    return render(
        request, 'my_view/indexFront.html',
        context={'num_visits': num_visits}
    )


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/todo/my_view/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)

            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()

            user_pomodoro = Pomodoro()
            user_pomodoro.user = new_user
            user_pomodoro.count = 0
            user_pomodoro.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def my_view(request):
    return render(request, 'my_view/indexFront.html')


@login_required
def create_todo(request, pk):
    if request.method == "POST":
        todo = Todo()
        todo.todo_title = pk
        todo.performer = request.user
        todo.save()
        data = serializers.serialize('json', Todo.objects.filter(performer=request.user), fields=('pk', 'todo_title'))
        return JsonResponse(data,  safe=False)


def delete(request, pk):
    try:
        person = Todo.objects.get(pk=pk)
        person.delete()
        data = serializers.serialize('json', Todo.objects.filter(performer=request.user))
        return JsonResponse(data, safe=False)
    except Todo.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


@login_required
def delete_all(request):
    try:
        all_todo = Todo.objects.filter(performer=request.user)
        all_todo.delete()
        return HttpResponseRedirect("/todo")
    except Todo.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


@login_required
def edit(request, pk, new):
    try:
        todo = Todo.objects.get(pk=pk)
        if request.method == "POST":
            todo.todo_title = new
            todo.save()
            data = serializers.serialize('json', Todo.objects.filter(performer=request.user))
            return JsonResponse(data, safe=False)
    except Todo.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


@login_required
def all_user_data(request):
    select_data = [*Todo.objects.filter(performer=request.user), *Pomodoro.objects.filter(user=request.user)]
    serializer = serializers.serialize('json', select_data, fields=('pk', 'todo_title', 'count'))
    return JsonResponse(serializer, safe=False)


@login_required
def pomodoro_count(request, pk):
    if request.method == "POST":
        pomodoro = Pomodoro.objects.get(user=request.user)
        if pk == 'add':
            pomodoro.count += 1
        elif pk == 'delete':
            pomodoro.count = 0
        pomodoro.save()

        data = {'count': pomodoro.count}
        return JsonResponse(data)
