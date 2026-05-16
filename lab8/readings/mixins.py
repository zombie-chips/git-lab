from django.contrib.auth.mixins import UserPassesTestMixin

class ObserverRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.role in ['observer', 'meteorologist', 'admin']

class MeteorologistRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.role in ['meteorologist', 'admin']

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'admin'

class CanEditReadingMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'admin':
            return True
        reading = self.get_object()
        return reading.created_by == self.request.user