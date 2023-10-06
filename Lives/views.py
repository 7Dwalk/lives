from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse


# Authenticate methods
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Проверка на уникальность username и email
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already exists'})

        # Создание нового пользователя
        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.save()

        return JsonResponse({'success': True, 'message': 'Registration successful'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Проверка наличия пользователя с указанным username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid username'})

        if not user.check_password(password):
            # Проверка пароля
            return JsonResponse({'success': False, 'message': 'Invalid password'})

        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user:
            # Вход пользователя
            login(request, authenticated_user)
            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Unable to login'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

