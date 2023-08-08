from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone


class UserType(models.TextChoices):
    STAFF = "STAFF", "Staff"
    CUSTOMER = "CUSTOMER", "Customer"
    BANKER = "BANKER", "Banker"
    PROVIDER = "PROVIDER", "Provider"


class UserManager(BaseUserManager):
    def create_user(
        self, first_name, last_name, email, username, password, **extra_fields
    ):
        """Manager method for creating new users

        Args:
            first_name (str): user's first name
            last_name (str): user's last name
            email (_str): user's unique email
            username (str): user's unique username
            password (str): user's raw password

        Raises:
            ValueError: first_name, last_name, username and email must be provided

        Returns:
            User: an instance of User model
        """
        if not username:
            raise ValueError("username must be provided")

        user: User = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_banker_user(
        self, first_name, last_name, email, username, password, **extra_fields
    ):
        extra_fields.setdefault("user_type", UserType.BANKER)

        return self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )

    def create_provider_user(
        self, first_name, last_name, email, username, password, **extra_fields
    ):
        extra_fields.setdefault("user_type", UserType.PROVIDER)

        return self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )

    def create_superuser(
        self, first_name, last_name, email, username, password, **extra_fields
    ):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    user_type = models.CharField(
        _("user type"), max_length=12, choices=UserType.choices, default=UserType.STAFF
    )
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return f"{self.username}"

    @property
    def is_authenticated(self):
        # Required to implement django's user-model interface
        return True

    def has_perm(self, perm, obj=None):
        # Required to implement django's user-model interface
        return True

    def has_perms(self, perm_list, obj=None):
        # Required to implement django's user-model interface
        return True

    def has_module_perms(self, app_label):
        # Required to implement django's user-model interface
        return True
