from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "authapp/index.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     return context
