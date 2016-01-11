from test_plus import TestCase

from ..forms import PinForm, LoginForm
from ..factories import UserFactory


class PinFormTest(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_clean_success(self):
        form = PinForm({'number': self.user.number, 'password': '1234'})
        self.assertEqual(form.is_valid(), True)

    def test_clean_wrong_pin(self):
        form = PinForm({'number': self.user.number, 'password': '12312214'})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors.as_data()['__all__'][0].message, "Wrong pin code")

    def test_clean_wrong_number(self):
        form = PinForm({'number': 16*'1', 'password': '12312214'})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors.as_data()['__all__'][0].message, "Wrong pin code")


class LoginFormTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_clean_success(self):
        form = LoginForm({'number': self.user.number})
        self.assertEqual(form.is_valid(), True)

    def test_wrong_number(self):
        form = LoginForm({'number': 16*'4'})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors.as_data()['__all__'][0].message, "Such card does not exist")
