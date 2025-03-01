from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.views.generic import TemplateView, View, ListView
from users.models import User
from authapp.forms import InviteCodeForm
from django.contrib import messages


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "authapp/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        invited_users_count = User.objects.filter(invited_by=user).count()
        context["user"] = user
        context["invited_users_count"] = invited_users_count

        return context


class EnterInviteCodeView(View):

    def post(self, request):
        invite_code = request.POST.get('invite_code')
        user = request.user
        invited_user = User.objects.filter(invite_code=invite_code).first()

        # Проверка, не является ли введённый код собственным
        if invite_code == user.invite_code:
            messages.error(request, "Вы не можете использовать свой собственный код приглашения.")
            return redirect('authapp:index')

        if invited_user:
            user.invited_by = invited_user
            user.save()
            return redirect('authapp:index')
        else:
            messages.error(request, "Пользователь с таким кодом не найден.")
            return redirect('authapp:index')


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "authapp/users_list.html"

    def dispatch(self, request, *args, **kwargs):
        # проверяем права
        user = self.request.user
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden(
            "Вы не можете просматривать/изменять/удалять этот объект."
        )
