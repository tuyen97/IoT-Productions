import uuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyMemberManager(BaseUserManager):
    def create_user(self, email, name, card_id, password='password'):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            card_id=card_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class Member(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('member name', max_length=30)
    email = models.EmailField(unique=True)
    card_id = models.CharField('card id', unique=True, max_length=20)
    course = models.CharField('course', null=True, max_length=10)
    registered_day = models.DateField(auto_now_add=True)
    avatar = models.ImageField(null=True, upload_to='avatar')
    research_about = models.TextField('research', null=True)
    is_train = models.BooleanField(default=False)
    threshold = models.IntegerField(null=True)
    is_in_lab = models.BooleanField(default=False,null=False)
    coefficient = models.IntegerField('coefficients salary', default=1)
    password = models.CharField('password', default='password', max_length=20)
    is_enough_images = models.BooleanField(default=False)
    is_added_to_blockchain = models.BooleanField(default=False)
    number_of_train_images = models.IntegerField(default=0)

    objects = MyMemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'card_id']

    # This is what you would increment on save
    # Default this to one as a starting point
    recognize_label = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = Member.objects.all().aggregate(largest=models.Max('recognize_label'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest)
            # and add one to it
            if last_id is not None:
                self.recognize_label = last_id + 1

        super(Member, self).save(*args, **kwargs)

    STUDENT = 'ST'
    TEACHER = 'TE'
    POSITION_IN_LAB_CHOICES = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher')
    )
    position = models.CharField(
        max_length=2,choices=POSITION_IN_LAB_CHOICES,default=STUDENT
    )

    def __str__(self):
        return self.name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # All teacher are staff
        return self.position == self.TEACHER


class Logs(models.Model):
    time_stamp = models.DateTimeField('Time member in/out', primary_key=True)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    is_go_in = models.BooleanField(null=True)
    result_auth = models.BooleanField(null=True)
    image = models.ImageField(upload_to='logs/%Y/%m/%d')
    unlock_server_room = models.IntegerField(null=True)

    # def __str__(self):
    #     return self.time_stamp


class Money(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    total_hour = models.IntegerField('Hour per day', null=False)
    date = models.DateField(null=False)
