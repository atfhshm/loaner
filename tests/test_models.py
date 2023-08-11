from django.test import TestCase
from faker import Faker

from users.models import User
from funds.models import Fund

fake = Faker()


class TestUserManager(TestCase):
    def setUp(self) -> None:
        return super().setUp()


class UserTestCase(TestCase):
    def setUp(self):
        self.username = fake.user_name()
        self.user: User = User.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            username=self.username,
            user_type="CUSTOMER",
            password=fake.password(),
        )

    def test_str_method(self):
        self.assertEqual(self.user.__str__(), self.username)

    def test_is_authenticated_method(self):
        self.assertTrue(self.user.is_authenticated)

    def test_has_perm_method(self):
        self.assertTrue(self.user.has_perm([]))

    def test_has_perms_method(self):
        self.assertTrue(self.user.has_perms([]))

    def test_has_module_perms_method(self):
        self.assertTrue(self.user.has_module_perms("users"))

    def test_create_user(self):
        user = User.objects.create_user(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            username=fake.user_name(),
            user_type="CUSTOMER",
            password=fake.password(),
        )
        self.assertIsInstance(user, User)
        user.delete()

    def test_create_user_raises_value_error(self):
        self.assertRaises(
            ValueError,
            User.objects.create_user,
            username="",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            user_type="CUSTOMER",
            password=fake.password(),
        )

    def test_create_banker_user(self):
        user = User.objects.create_banker_user(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            username=fake.user_name(),
            password=fake.password(),
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_type, "BANKER")

    def test_create_provider_user(self):
        user = User.objects.create_provider_user(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            username=fake.user_name(),
            password=fake.password(),
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_type, "PROVIDER")

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            username=fake.user_name(),
            password=fake.password(),
        )
        self.assertEqual(user.user_type, "STAFF")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertIsInstance(user, User)

    def tearDown(self):
        self.user.delete()
