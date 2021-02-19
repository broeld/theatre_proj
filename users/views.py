from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View

from .forms import LoginForm, RegistrationForm
from .models import Customer


class LoginView(View):
    form = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('plays:home')

        context = {'form': self.form, 'message': ''}
        return render(request, 'account/login.html', context=context)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user_info = form.cleaned_data
            user = authenticate(username=user_info['username'], password=user_info['password'])
        else:
            return HttpResponse(status=404)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('plays:home')
            message = "Login is not active"
        else:
            message = "Wrong login or password"

        context = {'form': self.form, 'message': message}
        return render(request, 'account/login.html', context=context)


class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return redirect('plays:home')


class PasswordChangeView(View, LoginRequiredMixin):
    form = PasswordChangeForm

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')

        form = self.form(request.user)
        context = {'form': form, 'messages': []}
        return render(request, 'account/password_change_form.html', context=context)

    def post(self, request):
        form = self.form(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get('new_password1')

            user.set_password(password)
            user.save()

            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect('plays:home')

        messages = list(form.error_messages.values())
        form = self.form(request.user)
        context = {'form': form, 'messages': messages}
        return render(request, 'account/password_change_form.html', context=context)


class PasswordResetView(View):
    form = PasswordResetForm
    template_name = 'account/password_reset_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('users:password-change')

        context = {'form': self.form, 'messages': []}
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # if email is None:
            #     return user does not exists handler
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                context = {'form': self.form, 'messages': ['User with this email doesn\'t exists.']}
                return render(request, self.template_name, context=context)

            request.session['email'] = email
            return redirect(reverse('users:password-reset-set'))

        messages = ["you have entered invalid information"]
        context = {'form': self.form, 'messages': messages}
        return render(request, self.template_name, context=context)


class PasswordResetDone(View):
    template_name = 'account/password_reset_done.html'

    def get(self, request):
        return render(request, self.template_name)


class PasswordResetSet(View):
    form = SetPasswordForm
    template_name = 'account/password_reset_set.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('plays:home')

        user = self.user_get(request)
        form = SetPasswordForm(user)
        context = {'form': form, 'messages': []}
        return render(request, self.template_name, context=context)

    def post(self, request):
        user = self.user_get(request)
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data.get('new_password1')
            user.set_password(password)
            user.save()

            return redirect('users:password-reset-done')
        else:
            messages = form.error_messages.values()

        context = {'form': self.form, 'messages': messages}
        return render(request, self.template_name, context=context)

    def user_get(self, request):
        email = request.session['email']
        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            # create user does not exists mistake view / return
            return


class UserRegistration(View):
    form = RegistrationForm
    template_name = 'account/signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('plays:home')

        context = {'form': self.form, 'message': ''}
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                User.objects.get(email=email)
                context = {'form': self.form, 'message': "User with this email is already exists"}
                return render(request, self.template_name, context=context)
            except User.DoesNotExist:
                user = form.save()

            user.refresh_from_db()

            user.customer.first_name = form.cleaned_data.get('first_name')
            user.customer.last_name = form.cleaned_data.get('last_name')
            user.customer.email = form.cleaned_data.get('email')

            user.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('plays:home')
        else:
            messages = form.error_messages.values()
            context = {'form': self.form, 'message': messages}
            return render(request, self.template_name, context=context)


class UserPageView(View):
    template_name = 'account/user_page.html'

    def get(self, request):
        if not request.user.is_authenticated:
            redirect('users:login')

        user = request.user
        if user:
            try:
                customer = Customer.objects.get(user=user)
            except Customer.DoesNotExist:
                return redirect('plays:home')
            #
            # try:
            #     tickets = customer.ticket_set.all().order_by('play__date')
            # except AttributeError:
            #     tickets = []

            context = {'customer': customer}
            return render(request, self.template_name, context=context)