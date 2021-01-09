from django.contrib import messages
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from main.models import Channel, User, WorkSpace, UserChannel, UserWorkSpace
from main.forms import LoginForm, UserForm, WorkSpaceForm, ChannelForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, reverse, redirect
from django.utils import timezone
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from django.core.mail import send_mail
import json
import string
from random import *


def login(request):
    try:
        if request.session['_auth_login']:
            return home(request)
    except:
        try:
            if request.POST['submit']:
                user = authenticate(request.POST['username'], request.POST['password'])
                if user is None:
                    return render(request, 'login.html', {'message': 'Incorrect username or password'})
                else:
                    request.session['_auth_user_email'] = user.email
                    request.session['_auth_user_name'] = user.name
                    request.session['_auth_login'] = True
                    return home(request)
        except Exception as ex:
            return render(request, 'login.html', {'message': ""})


def logout(request):
    try:
        request.session.flush()
        return redirect("../")
    except Exception as ex:
        print(ex)
        return redirect("../")


def signup(request):
    try:
        if request.POST['submit']:
            try:
                user = User.objects.get(email=request.POST['email'])
                return render(request, 'signup.html', {'message': 'User already exits'})
            except ObjectDoesNotExist:
                user = User(name=request.POST['name'], email=request.POST['email'], password=request.POST['password'], invited=False)
                user.save()
                return redirect('../')
    except Exception as ex:
        print(ex)
        return render(request, 'signup.html')


def authenticate(username, password):
    try:
        user = User.objects.get(email=username, password=password)
        return user
    except ObjectDoesNotExist:
        return None


def home(request):
    user = User.objects.get(email=request.session['_auth_user_email'])
    if user.invited:
        return redirect('reset/')
    user_workspaces = UserWorkSpace.objects.filter(user=User.objects.get(email=request.session['_auth_user_email']))
    user_channels = UserChannel.objects.filter(user=user)
    return render(request, 'hom3.html', {'user': user, 'workspaces': user_workspaces, 'channels': user_channels})


def home1(request, workspace, channel):
    user = User.objects.get(email=request.session['_auth_user_email'])
    if user.invited:
        return redirect('reset/')
    workspace = WorkSpace.objects.get(name=workspace)
    is_admin = UserWorkSpace.objects.get(user=user, workspace=workspace).privilege

    # fetch channels
    channels = []
    current_channel = None
    user_channels = UserChannel.objects.filter(user=user)
    print(user_channels)
    for user_channel in user_channels:
        try:
            channel_ = Channel.objects.get(pk=user_channel.channel.pk, workspace=workspace)
            channels.append(channel_)
            if channel_.name == channel:
                current_channel = channel_
        except ObjectDoesNotExist:
            pass

    if current_channel is None:
        raise Exception("niklo yaha se")

    # fetch channel users
    channel_users = UserChannel.objects.filter(channel=current_channel.pk)
    print(channel_users)

    # fetch workspace users
    workspace_users = UserWorkSpace.objects.filter(workspace=workspace)

    # fetch workspaces
    workspaces = UserWorkSpace.objects.filter(user=user)

    # fetch messages
    messarray = []
    es = Elasticsearch("192.168.43.177:9200")
    query = '{"query":{"match":{"channel":"' + str(current_channel.pk) + '"}}}'
    messages_ = es.search(index="messages", doc_type="message", body=query)
    messages_ = messages_['hits']['hits']
    for mess in messages_:
        temp = mess['_source']
        temp['id'] = mess['_id']
        messarray.append(temp)
    messarray = sorted(messarray, key=lambda k: k['timestamp'])
    return render(request, 'hom1.html', {'is_admin':is_admin, 'channels': channels, 'workspaces': workspaces, 'workspace': workspace, 'workspace_users':workspace_users, 'user': user, 'channel': current_channel, 'channel_users': channel_users, 'messarray': messarray})


def create_workspace(request):
    try:
        print(request.POST['workspace'])
        user = User.objects.get(email=request.session['_auth_user_email'])
        print(user)
        ws = WorkSpace(name=request.POST['workspace'], created_by=user, created_on=timezone.now())
        ws.save()
        print(ws)
        uw_rel = UserWorkSpace(user=user, workspace=ws, privilege=True)
        uw_rel.save()
        channel = Channel(name="general", workspace=ws, created_by=user, created_on=timezone.now())
        channel.save()
        cu_rel = UserChannel(channel=channel, user=user)
        cu_rel.save()
        print("done!")
        return redirect('../')
    except Exception as ex:
        print(ex)
        return redirect('../')


def add_channel_to_workspace(request, workspace, channel):
    try:
        user = User.objects.get(email=request.session['_auth_user_email'])
        workspace = WorkSpace.objects.get(name=workspace)
        new_channel = Channel(name=request.POST['channel'], workspace=WorkSpace.objects.get(name=workspace), created_by=user, created_on=timezone.now())
        new_channel.save()
        user_channel_rel = UserChannel(user=user, channel=new_channel)
        user_channel_rel.save()
        return redirect('../')
    except Exception as ex:
        print(ex)
        return redirect('../')


def add_user_to_channel(request, workspace, channel):
    try:
        user = User.objects.get(email=request.POST['user'])
        user_channel_rel = UserChannel(user=user, channel=Channel.objects.get(name=channel, workspace=WorkSpace.objects.get(name=workspace)))
        user_channel_rel.save()
        return redirect('../')
    except Exception as ex:
        print(ex)
        return redirect('../')


def add_user_to_workspace(request, workspace, channel):
    try:
        user = User.objects.get(email=request.POST['user'])
        workspace = WorkSpace.objects.get(name=workspace)
        user_workspace_rel = UserWorkSpace(user=user, workspace=workspace, privilege=request.POST.get('is_admin', False))
        user_workspace_rel.save()
        user_channel_rel = UserChannel(user=user, channel=Channel.objects.get(name='general', workspace=workspace))
        user_channel_rel.save()
        send_mail(
            "Invitation to join workspace",
            "You have been added to %s workspace." % workspace,
            "prince.mohitagrawal@gmail.com",
            [request.POST['user']],
            fail_silently=False,
        )
        return redirect('../')
    except ObjectDoesNotExist:
        min_char = 8
        max_char = 12
        allchar = string.ascii_letters + string.punctuation + string.digits
        password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        user = User(email=request.POST['user'], password=password, name="", invited=True)
        user.save()
        workspace = WorkSpace.objects.get(name=workspace)
        user_workspace_rel = UserWorkSpace(user=user, workspace=workspace, privilege=request.POST.get('is_admin', False))
        user_workspace_rel.save()
        user_channel_rel = UserChannel(user=user, channel=Channel.objects.get(name='general', workspace=workspace))
        user_channel_rel.save()
        send_mail(
            "Invitation to join workspace",
            "Here are your login credentials \n username: %s \n password: %s \n" %(request.POST['user'], password),
            "prince.mohitagrawal@gmail.com",
            [request.POST['user']],
            fail_silently=False,
        )
        return redirect('../')


def show_reply(request):
    if request.method == 'GET':
        message_id = request.GET['message_id']
        messarray = []
        es = Elasticsearch("192.168.43.177:9200")
        query = '{"query":{"match":{"reply_to":"' + message_id + '"}}}'
        messages_ = es.search(index="messages", doc_type="message", body=query)
        messages_ = messages_['hits']['hits']
        for mess in messages_:
            temp = mess['_source']
            temp['id'] = mess['_id']
            messarray.append(temp)
        messarray = sorted(messarray, key=lambda k:k['timestamp'])
        return HttpResponse(json.dumps(messarray), content_type="application/json")
    else:
        return HttpResponse("Something wrong")


def change_password(request):
    user = User.objects.get(email=request.session['_auth_user_email'])
    try:
        if request.POST['submit']:
            user.name = request.POST['name']
            user.password = request.POST['password']
            user.invited = False
            user.save()
            return redirect("../")
        return render(request, 'hom2.html', {'user': user})
    except Exception as ex:
        print(ex)
        return render(request, 'hom2.html', {'user': user})

"""
class SignUpView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'signup.html'
    success_url = '../'


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '../'

    def authenticate(self, username, password):
        try:
            user = User.objects.get(email=username, password=password)
            return user
        except ObjectDoesNotExist:
            return None

    def form_valid(self, form):
        user = self.authenticate(self.request.POST['username'], self.request.POST['password'])
        if user is None:
            return render(self.request, 'login.html', self.get_context_data())
        self.request.session['_auth_user_email'] = user.email
        self.request.session['_auth_user_name'] = user.name
        return super(LoginView, self).form_valid(form)


class CreateWorkSpace(CreateView):
    model = WorkSpace
    form_class = WorkSpaceForm
    template_name = 'form_templates.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.created_by = User.objects.get(email=self.request.session['_auth_user_email'])
        form.instance.created_on = timezone.now()
        return super(CreateWorkSpace, self).form_valid(form)


class CreateChannel(CreateView):
    model = Channel
    form_class = ChannelForm
    template_name = 'form_templates.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.created_by = User.objects.get(email=self.request.session['_auth_user_email'])
        form.instance.created_on = timezone.now()
        return super(CreateChannel, self).form_valid(form)


class WorkSpaceList(ListView):
    model = WorkSpace
    template_name = 'list_templates.html'
"""
