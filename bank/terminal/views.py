from django.views.generic import TemplateView


class CardView(TemplateView):
    template_name = 'terminal/card.html'
