from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from django.contrib.auth.models import User



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def home(request):
    return render(request, 'blog/home.html')


def pentest(request):
    pentest_category = Category.objects.get(name='pentest')
    posts = pentest_category.posts.all()
    return render(request, 'blog/pentest.html', {'posts': posts})


def security(request):
    security_category = Category.objects.get(name='security')
    posts = security_category.posts.all()
    return render(request, 'blog/security.html', {'posts': posts})


from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Хэширование пароля
            user.save()
            login(request, user)  # Авторизация пользователя
            return redirect('profile')  # Перенаправление на страницу профиля
    else:
        form = UserRegistrationForm()
    
    return render(request, 'blog/register.html', {'form': form})



from django.contrib import messages
from .forms import UserLoginForm

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправление после входа
            else:
                messages.error(request, "Логин не существует и/или неправильный пароль.")
        else:
            messages.error(request, "Ошибка в данных формы.")
    else:
        form = UserLoginForm()
    
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Перенаправление после выхода


from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

### Чтобы обрабатывать отображение профиля пользователя и изменения пароля
@login_required
def profile_view(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        image_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return redirect('profile')
        
        if image_form.is_valid():
            image_form.save()
            return redirect('profile')
    else:
        password_form = PasswordChangeForm(user=request.user)
        image_form = ProfileImageForm(instance=request.user.profile)
    
    return render(request, 'blog/profile.html', {
        'password_form': password_form,
        'image_form': image_form
    })



from django import forms
from .models import Profile

# форма для загрузки/изменения изображения в профиле пользователя
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
