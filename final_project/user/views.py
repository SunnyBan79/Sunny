from unicodedata import name
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm

User = get_user_model()


def index(request):
    user = User.objects.filter(id=request.user.id).first()
    usernames = user.username if user else "Anonymous User!"
    return render(request, "index.html", {"welcome_msg": f"Hello,{usernames}"})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: 2. login 할 때 form을 활용해주세요
        form = LoginForm(request.POST)
        if form.is_valid():
            raw_username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            msg = "올바른 유저ID와 패스워드를 입력하세요."
            try:
                user = User.objects.get(username=raw_username)
            except User.DoesNotExist:
                msg = "올바른 유저ID와 패스워드를 입력하세요."
            else:
                if user.check_password(raw_password):
                    msg = None
                    login(request, user)
                    return redirect("index")
    else:
        msg = None
        form = LoginForm()
    return render(request, "login.html", {"form": form, "error": msg})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요	
    logout(request)					
    return redirect("index")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
@login_required(login_url='/login')
def user_list_view(request):
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    page = int(request.GET.get("p", 1))
    users = User.objects.all().order_by("-id")
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)
    return render(request, "users.html", {"users": users})
