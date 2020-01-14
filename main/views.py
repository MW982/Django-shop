from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.timezone import now

from uuid import uuid4

from main.forms import NewUserForm, ForgotForm, PassForm, UserDataForm
from main.models import User


SITE = "127.0.0.1:8000"
EMAIL = "justemaildjango@gmail.com"


def send_activation_email(username):
    user = User.objects.get(username=username)
    email_to = user.email
    title = f"Hello {username}"
    link_active = user.linkID
    message = (
        f"Here is your activation link. \n Link: http://{SITE}/active/{link_active}"
    )
    res = send_mail(title, message, EMAIL, [email_to])


def register_view(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                messages.error(request, f"{email} is already registered!")
                return redirect("main:register")

            user = form.save()
            sendActivationEmail(username)
            return redirect("product:homepage")

    form = NewUserForm
    return render(request, "main/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.activated:
                messages.error(request, "Activate your account!")
                # change to notactivated page
                return redirect("product:homepage")
            login(request, user)
            return redirect("product:homepage")
    else:
        form = AuthenticationForm

    return render(request, "main/login.html", {"form": form})


@login_required
def account_view(request):
    return render(request, "main/account.html", {})


@login_required
def account_settings_view(request):
    if request.method == "POST":
        form = UserDataForm(data=request.POST)
        if form.is_valid():
            user = User.objects.all().get(username=form.cleaned_data["username"])
            user.first_name = form.cleaned_data["name"]
            user.last_name = form.cleaned_data["lastname"]
            user.phone_number = form.cleaned_data["number"]
            user.address = form.cleaned_data["address"]

            user.save()

    form = UserDataForm
    return render(request, "main/accountSettings.html", {"form": form})


@login_required
def account_transactions_view(request):
    user = User.objects.all().get(username=request.user.username)
    record = []
    for transaction in user.record.all():
        record.append(transaction)
    context = {"record": record}

    return render(request, "main/accountTransactions.html", context)


@login_required
def transaction_detail_view(request, trans_id):
    user = User.objects.all().get(username=request.user.username)
    trans_record = user.record.get(id=trans_id)
    record = {}
    # for item in items:
    #     name = item[0]
    #     num = item[1]
    #     price = item[2]
    context = {"transRecord": trans_record}
    return render(request, "main/transactionDetail.html", context)


def logout_view(request):
    logout(request)
    return redirect("product:homepage")


def forgot_user_view(request):
    if request.method == "POST":
        form = ForgotForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = User.objects.filter(email=email)
            if user.exists():
                title = "Django Project"
                message = f"Your username is {user[0]}"
                send_mail(title, message, EMAIL, [email])
                return redirect("product:homepage")

    form = ForgotForm
    return render(request, "main/forgot.html", {"form": form})


def forgot_pass_view(request):
    if request.method == "POST":
        form = ForgotForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = User.objects.filter(email=email)
            if user.exists():
                u = User.objects.get(email=email)
                u.linkID = uuid4()
                u.resetTime = now()
                u.save()
                #    print(u.resetTime)
                #    print(u.linkID)
                title = "Django Project"
                link = f"http://{SITE}/forpass/{u.linkID}"
                message = f"Reset password (Link lasts for 30 mins) -> {link}"
                send_mail(title, message, EMAIL, [email])
                return redirect("product:homepage")

    form = ForgotForm
    return render(request, "main/forgot.html", {"form": form})


def change_pass_view(request, k_user):
    return render(request, "main/changePass.html", {"user": user})


def reset_pass_view(request, resetUUID):
    try:
        user = User.objects.get(linkID=resetUUID)
    except ObjectDoesNotExist:
        return redirect("product:homepage")
    #    print(now() - user.resetTime )
    tdiff = now() - user.resetTime
    tdiff = tdiff.total_seconds()

    if not tdiff >= 1800:
        if request.method == "POST":
            form = PassForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data.get("password1")
                user.set_password(password)
                user.linkID = uuid4()
                user.save()
                return redirect("main:account")
            else:
                print("resetPass form is invalid")

        form = PassForm
        return render(request, "main/resetPass.html", {"form": form})

    return redirect("product:homepage")


def activate_view(request, activateUUID):
    user = User.objects.get(linkID=activateUUID)
    user.activated = True
    user.save()

    return redirect("product:homepage")
