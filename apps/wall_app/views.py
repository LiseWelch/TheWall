from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt

def root(request) :
    return render(request, 'wall_app/root.html')

def delete(request, type, id):
    if type == 'message':
        message = Message.objects.get(id=id)
        message.delete()
    if type == 'comment':
        comment = Comment.objects.get(id=id)
        comment.delete()
    return redirect('/wall')

def post(request) :
    user = User.objects.get(id=request.session['userid'])
    Message.objects.create(message=request.POST['post'], user_id=user)
    return redirect('/wall')

def comment(request) :
    user = User.objects.get(id=request.session['userid'])
    message = Message.objects.get(id=request.POST['message_id'])
    Comment.objects.create(comment=request.POST['comment'], user_id=user, message_id=message)
    return redirect('/wall')

def login(request) :
    if request.POST['type']=="register" :
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items() :
                messages.error(request,value)
            return redirect('/')
        else :
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=request.POST['first_name'],
                                last_name=request.POST['last_name'],
                                email=request.POST['email'],
                                password=pw_hash
            )
            user = User.objects.last()
            request.session['userid'] = user.id
            return redirect('/wall')
    elif request.POST['type']=="login" :
        user = User.objects.filter(email=request.POST['email'])
        if user :
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id 
                return redirect('/wall')
            else :
                messages.error(request,"E-mail or Password is incorrect")
    return redirect('/')

def logout(request) :
    del request.session['userid']
    return redirect('/')

def wall(request) :
    context = {
        'user' : User.objects.get(id=request.session['userid']),
        'messages': Message.objects.all().order_by("-created_at"),
        'comments': Comment.objects.all().order_by("-created_at")
    }
    return render(request, 'wall_app/wall.html', context)