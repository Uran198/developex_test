from django.core.urlresolvers import reverse
from django.test import mock, RequestFactory

from test_plus import TestCase

from .. import views
from ..factories import UserFactory


class LoginViewTest(TestCase):

    def setUp(self):
        self.view = views.LoginView()

    def test_get_success_url(self):
        self.view.number = 16*'2'
        self.assertEqual(self.view.get_success_url(),
                         reverse('terminal:pin', kwargs={'number': 16*'2'}))

    def test_form_valid(self):
        user = UserFactory()
        f = self.view.get_form_class()({'number': user.number})
        self.assertEqual(f.is_valid(), True)
        self.view.form_valid(f)
        self.assertEqual(self.view.number, user.number)

    @mock.patch('bank.terminal.views.redirect')
    def test_dispatch(self, mock):
        request = RequestFactory().get('fake')
        request.user = UserFactory()
        self.view.dispatch(request)
        self.assertEqual(len(mock.mock_calls), 1)


class PinViewTest(TestCase):

    def setUp(self):
        self.view = views.PinView()

    def test_get_initial(self):
        self.view.kwargs = {'number': '10'}
        self.assertDictEqual(self.view.get_initial(), {'number': '10'})

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(), reverse('terminal:operations'))

    @mock.patch('bank.terminal.views.login')
    def test_form_valid(self, mock):
        user = UserFactory()
        f = self.view.get_form_class()({'number': user.number, 'password': '1234'})
        self.assertEqual(f.is_valid(), True)
        self.view.request = RequestFactory().post('/fake')
        self.view.form_valid(f)
        self.assertEqual(len(mock.mock_calls), 1)


class LogoutViewTest(TestCase):

    def setUp(self):
        self.view = views.LogoutView()

    @mock.patch('bank.terminal.views.logout')
    def test_post(self, mock):
        self.view.request = RequestFactory().post('/fake')
        self.view.post(self.view.request)
        self.assertEqual(len(mock.mock_calls), 1)


class WithdrawMoneyViewTest(TestCase):

    def setUp(self):
        self.view = views.WithdrawMoneyView()
        self.factory = RequestFactory()

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(), reverse('terminal:operations'))

    def test_get_for_kwargs(self):
        request = self.factory.get('fake/')
        request.user = UserFactory()
        self.view.request = request
        kwargs = self.view.get_form_kwargs()
        self.assertEqual(kwargs['instance'], request.user)

    def test_form_valid(self):
        user = UserFactory(balance=100)
        form = self.view.get_form_class()({'amount': 20}, instance=user)
        self.assertEqual(form.is_valid(), True)
        self.view.form_valid(form)
        user.refresh_from_db()
        self.assertEqual(user.balance, 80)
