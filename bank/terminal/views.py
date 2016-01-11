from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView, TemplateView, RedirectView
from django.contrib.auth import login, logout

from braces.views import LoginRequiredMixin

from .forms import PinForm, LoginForm, WithdrawMoneyForm
from .models import Transaction


class LoginView(FormView):
    template_name = 'terminal/login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('terminal:operations')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('terminal:pin', kwargs={'number': self.number})

    def form_valid(self, form):
        self.number = form.cleaned_data['number']
        return super(LoginView, self).form_valid(form)


class PinView(FormView):
    template_name = 'terminal/pin.html'
    form_class = PinForm

    def get_success_url(self):
        return reverse('terminal:operations')

    def get_initial(self):
        initial = super(PinView, self).get_initial()
        initial['number'] = self.kwargs.pop('number')
        return initial

    def form_valid(self, form):
        login(self.request, form.user)
        return super(PinView, self).form_valid(form)


class LogoutView(RedirectView):
    http_method_names = [u'post']
    permanent = False
    url = '/'

    def post(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).post(request, *args, **kwargs)


class OperationsView(LoginRequiredMixin, TemplateView):
    template_name = 'terminal/operations.html'


class WithdrawMoneyView(LoginRequiredMixin, FormView):
    template_name = 'terminal/withdraw.html'
    form_class = WithdrawMoneyForm

    def get_success_url(self):
        return reverse('terminal:operations')

    def get_form_kwargs(self):
        kwargs = super(WithdrawMoneyView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(WithdrawMoneyView, self).form_valid(form)


class ShowBalanceView(LoginRequiredMixin, TemplateView):
    template_name = 'terminal/balance.html'

    def get(self, request, *args, **kwargs):
        Transaction.objects.create(
            operation='CB',
            card=request.user,
        )
        return super(ShowBalanceView, self).get(request, *args, **kwargs)
