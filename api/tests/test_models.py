from django.test import TestCase
from django.core.exceptions import ValidationError

from api.models import MyUser, Tag


class MyUserModelTest(TestCase):

    def test_save_user(self):
        u = MyUser(gender='M', email='a@b.com', password='abc',
                   first_name='John', last_name='Doe')
        u.save()
        u.full_clean()
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(u.get_full_name(), 'John Doe')
        self.assertEqual(u.get_short_name(), 'John')

    def test_create_user(self):
        # normal usage
        u = MyUser.objects.create_user(email='a@b.com', password='aaa', gender='F', first_name='Jane', last_name='Doe')
        u.full_clean()
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(u.is_admin, False)
        self.assertEqual(u.is_active, True)

        # cannot create super user, even if requested
        u = MyUser.objects.create_user(email='3@b.com', password='aaa',
            gender='F', first_name='Jane', last_name='Doe', is_admin=True)
        self.assertEqual(u.is_admin, False)
        self.assertEqual(u.is_active, True)
        u.full_clean()
        self.assertEqual(MyUser.objects.count(), 2)


class TagModelTest(TestCase):

    def test_save_duplicate_fails(self):
        Tag.objects.create(name='programmer')
        t2 = Tag(name='programmer')
        with self.assertRaises(ValidationError) as context:
            t2.full_clean()
        self.assertTrue('Tag with this Name already exists.' in
                         str(context.exception))
        self.assertEqual(Tag.objects.count(), 1)

    def test_many2many(self):
        t1 = Tag.objects.create(name='programmer')
        t2 = Tag.objects.create(name='joker')
        u1 = MyUser.objects.create_user(email='1@b.com', gender='M',
            first_name='a', last_name='b')
        u2 = MyUser.objects.create_user(email='2@b.com', gender='M',
            first_name='a', last_name='b')
        u1.tags.add(t1)
        u1.tags.add(t2)
        u2.tags.add(t2)
        self.assertEqual(list(u1.tags.all()), [t1, t2])
        self.assertEqual(list(u2.tags.all()), [t2])
        # reverse look up
        self.assertEqual(list(t1.myuser_set.all()), [u1])
        self.assertEqual(list(t2.myuser_set.all()), [u1, u2])
