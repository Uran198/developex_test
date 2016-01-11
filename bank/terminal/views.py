from django.core.urlresolvers import reverse
from django.views.generic import FormView, TemplateView
from django.contrib.auth import login

from .forms import PinForm, LoginForm


class LoginView(FormView):
    template_name = 'terminal/login.html'
    form_class = LoginForm

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


class OperationsView(TemplateView):
    template_name = 'terminal/operations.html'
