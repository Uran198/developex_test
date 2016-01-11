from test_plus import TestCase

from ..forms import PinForm, LoginForm, WithdrawMoneyForm
from ..factories import UserFactory
from ..models import Transaction


class PinFormTest(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_clean_success(self):
        form = PinForm({'number': self.user.number, 'password': '1234'})
        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.user, self.user)

    def test_clean_wrong_pin(self):
        form = PinForm({'number': self.user.number, 'password': '12312214'})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors.as_data()['__all__'][0].message, "Wrong pin code")

    def test_clean_wrong_number(self):
        form = PinForm({'number': 16*'1', 'password': '12312214'})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors.as_data()['__all__'][0].message, "Wrong pin code")

    def test_blocked_number(self):
        self.user.is_blocked = True
        self.user.save()
        form = PinForm({'number': self.user.number, 'password': '1234'})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors.as_data()['__all__'][0].message, "The card is blocked")

    def test_4_wrong_tries(self):
        for _ in range(4):
            form = PinForm({'number': self.user.number, 'password': '1235'})
            form.is_valid()
        self.user.refresh_from_db()
        self.assertEqual(self.user.is_blocked, True)

    def test_3_wrong_tries(self):
        for _ in range(3):
            form = PinForm({'number': self.user.number, 'password': '1235'})
            form.is_valid()
        self.user.refresh_from_db()
        self.assertEqual(self.user.wrong_tries, 3)
        self.assertEqual(self.user.is_blocked, False)

    def test_reseting_wrong_tries(self):
        form = PinForm({'number': self.user.number, 'password': '1235'})
        form.is_valid()
        self.user.refresh_from_db()
        self.assertEqual(self.user.wrong_tries, 1)
        form = PinForm({'number': self.user.number, 'password': '1234'})
        form.is_valid()
        self.user.refresh_from_db()
        self.assertEqual(self.user.wrong_tries, 0)


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

    def test_blocked_number(self):
        self.user.is_blocked = True
        self.user.save()
        form = LoginForm({'number': self.user.number})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors.as_data()['__all__'][0].message, "The card is blocked")


class WithdrawMoneyFormTest(TestCase):
    def setUp(self):
        self.user = UserFactory(balance=100)
        self.form = WithdrawMoneyForm

    def test_clean_too_much(self):
        form = self.form({'amount': 101}, instance=self.user)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors.as_data()['__all__'][0].message, "Insufficient balance")

    def test_clean_success(self):
        form = self.form({'amount': 100}, instance=self.user)
        self.assertEqual(form.is_valid(), True)

    def test_clean_too_little(self):
        form = self.form({'amount': -1}, instance=self.user)
        self.assertEqual(form.is_valid(), False)

    def test_no_instance(self):
        form = self.form({'amount': 102})
        self.assertEqual(form.is_valid(), True)

    def test_save(self):
        form = self.form({'amount': 20}, instance=self.user)
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 80)
        self.assertEqual(len(Transaction.objects.all()), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.operation, 'WD')
        self.assertEqual(transaction.card, self.user)
        self.assertEqual(transaction.amount, 20)
