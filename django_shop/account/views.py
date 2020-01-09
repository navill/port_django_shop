from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
# 유저 등록
# from account.actions import track_action
from account.forms import UserRegistrationForm, UserEditForm, UserProfileForm
# user 정보 변경
# edit이 실행되기 위해 인증이 미리 이루어져야 하기 때문에 @login_required를 사용
from account.models import Action, Profile
from order.models import Order

User = get_user_model()


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            # validation -> UserEditForm의 clean_<name> 메서드 실행
            user_form.save()
            # track_action(request.user, 'edited information')
            return redirect('shop:product_list')
        else:
            pass
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'account/edit.html', {'user_form': user_form})


# 사용자 등록
def register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():  # -> clean_<fieldname>() 실행 시점
            # user를 db에 저장하지 않고 인스턴스를 new_user에 할당-> 이후 set_password(), save() 호출
            new_user = user_form.save(commit=False)
            # 보안상 django의 set_password()를 거친 후 암호화된 비밀번호를 저장한다.
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # track_action(new_user, 'has created an account')
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


# history
@login_required
@staff_member_required
def get_history(request):
    page = request.GET.get('page')
    actions = Action.objects.all()
    paginator = Paginator(actions, 10)
    actions = paginator.get_page(page)
    return render(request, 'history/history.html', {'actions': actions})


@login_required
def change_password_done(request):
    # track_action(request.user, 'has changed password')
    return render(request, 'registration/password_change_done.html')


@login_required
def user_profile(request):
    user = User.objects.get(id=request.user.id)
    profile = None
    try:
        profile = Profile.objects.get(user=user)
    except Exception as e:
        print(f'Exception error: {e}')
    if request.method == 'POST':
        profile_form = UserProfileForm(instance=profile, data=request.POST)
        # profile_form = None
        if profile_form.is_valid():
            print('a')
            profile_form = profile_form.save(commit=False)
            # profile_form
            profile_form.user = user
            profile_form.save()
            # track_action(profile_form.user, 'has updated profile')
        return render(request, 'account/profile_done.html')
    else:
        if profile:
            profile_form = UserProfileForm(instance=profile)
        else:
            profile_form = UserProfileForm()
        user_orders = Order.objects.filter(user=request.user)
        return render(request, 'account/profile.html', {'profile_form': profile_form, 'user_orders': user_orders})
