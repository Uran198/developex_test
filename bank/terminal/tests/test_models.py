from test_plus import TestCase

from ..factories import UserFactory


class CardUserTest(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), '/')

    def test_get_username(self):
        self.assertEqual(self.user.get_username(), self.user.number)
