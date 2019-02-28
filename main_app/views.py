from django.views.generic import TemplateView


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass


class ProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass


class AuthView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass


class RegisterView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass


class AddPostView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass


class EditPostView(TemplateView):
    def get(self, request, *args, **kwargs):
        pass
