from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib.auth.decorators import login_required


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Usuário registrado com sucesso!'
            )
            return redirect('contact:login')
        else:
            messages.error(
                request,
                'O formulário possui algum um erro!'
            )

    return render(
        request,
        'contact/register.html',
        {
            'form': form,
            'mode': 'Register',
        }
    )


def login_view(request):

    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            print(f'login realizado: {user}')
            messages.success(request, f'Bem vindo, {user}')
            return redirect(
                        "contact:index"
                    )
        messages.error(request, 'Login inválido')

    return render(
        request,
        'contact/login.html',
        {
            'form': form,
            'mode': 'Login',
        }
    )


@login_required(login_url='contact:login')
def logout_view(request):
    auth.logout(request)
    print('logout realizado')
    return redirect(
        'contact:login'
    )


@login_required(login_url='contact:login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method != 'POST':

        return render(
            request,
            'contact/register.html',
            {
                'form': form,
                'mode': 'User Update',
            }
        )

    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'contact/register.html',
            {
                'form': form,
                'mode': 'User Update',

            }
        )
    form.save()
    messages.success(request, f'Atualizado com sucesso.')
    return redirect('contact:user_update')
