from django.test import mock
from django.views.generic import FormView

from test_plus import TestCase

from ..mixins import RenderErrorMixin


class Dummy(RenderErrorMixin, FormView):
    pass


class RenderErrorMixinTest(TestCase):

    def setUp(self):
        self.view = Dummy()
        self.view.request = mock.Mock()

    def test_form_invalid(self):
        form = mock.Mock()
        response = self.view.form_invalid(form)
        self.assertDictContainsSubset({'form': form}, response.context_data)
