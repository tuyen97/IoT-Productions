from pas.models import Member


class PasBackend:

    def authenticate(self, email=None, password=None):
        try:
            user = Member.objects.get(email=email, password=password)
            return user
        except Member.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Member.objects.get(id=user_id)
        except Member.DoesNotExist:
            return None
