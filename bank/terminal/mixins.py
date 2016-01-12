class RenderErrorMixin(object):

    def form_invalid(self, form):
        context = self.get_context_data()
        context.setdefault('form', form)
        return self.response_class(
            request=self.request,
            template='terminal/error.html',
            context=context,
            using=self.template_engine,
            content_type=self.content_type,
        )
