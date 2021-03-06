from __future__ import unicode_literals
from django.test import TestCase, Client
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Post, Wanted
from io import BytesIO
import datetime, random
from PIL import Image, ImageDraw, ImageFont
from .forms import PostForm, WantedForm, NameSearchForm, UserCreateForm, LoginForm
from .views import post, wishlist_add
# Create your tests here.
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (255, 255, 255)]
def get_image(n):
    screen = (200, 200)
    pen_color = random.choice(colors)
    bg_color = random.choice(colors)
    img = Image.new('RGB', screen, bg_color)
    x, y = img.size
    u = x - 1
    v = y - 1
    draw = ImageDraw.Draw(img)
    draw.line((0, 0, u, 0), pen_color)
    filename = "/sample_{}.jpg".format(n)
    img.save("media"+filename)
    return filename

def get_post_image_dict():
    img_file = BytesIO()
    img = Image.new('RGBA', size=(10,10), color=(255, 255, 255))
    img.save(img_file, 'png')
    img_file.name = 'test_post_img.png'
    img_file.seek(0)
    img_dict = {
        "post_images": SimpleUploadedFile(
            img_file.name,
            img_file.read(),
            content_type='image/png'
        )
    }
    return img_dict

def get_wanted_image_dict():
    img_file = BytesIO()
    img = Image.new('RGBA', size=(10,10), color=(255, 255, 255))
    img.save(img_file, 'png')
    img_file.name = 'test_wanted_img.png'
    img_file.seek(0)
    img_dict = {
        "wanted_images": SimpleUploadedFile(
            img_file.name,
            img_file.read(),
            content_type='image/png'
        )
    }
    return img_dict


class ClothesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        usr= cls.create_user()
        cls.create_post(usr)
        cls.create_wish(usr)
    @classmethod
    def create_user(cls):
        User(username="test", password="test", is_staff=True, is_active=True).save()
        usr = User.objects.filter(username='test').first()
        return(usr)
    @classmethod
    def create_post(cls, usr):
        Post(owner=usr, cloth_name='test1', item_info=1, brand_name='test1', season='test1', cloth_size='test1', \
            material='test1', price=1, buying_place='test1', buying_date=datetime.date.today(), post_images=get_image(1)).save()
        Post(owner=usr, cloth_name='test2', item_info=1, brand_name='test2', season='test2', cloth_size='test2', \
            material='test2', price=1, buying_place='test2', buying_date=datetime.date.today(), post_images=get_image(2)).save()
        Post(owner=usr, cloth_name='test3', item_info=1, brand_name='test3', season='test3', cloth_size='test3', \
            material='test3', price=1, buying_place='test3', buying_date=datetime.date.today(), post_images=get_image(3)).save()
        Post(owner=usr, cloth_name='test4', item_info=1, brand_name='test4', season='test4', cloth_size='test4', \
            material='test4', price=1, buying_place='test4', buying_date=datetime.date.today(), post_images=get_image(4)).save()
    @classmethod
    def create_wish(cls, usr):
        Wanted(owner=usr, wanted_cloth_name='test1', wanted_brand_name='test1', wanted_season='test1', wanted_price=1, \
            priority=1, wanted_images=get_image(5)).save()
        Wanted(owner=usr, wanted_cloth_name='test2', wanted_brand_name='test2', wanted_season='test2', wanted_price=1, \
            priority=1, wanted_images=get_image(6)).save()
        Wanted(owner=usr, wanted_cloth_name='test3', wanted_brand_name='test3', wanted_season='test3', wanted_price=1, \
            priority=1, wanted_images=get_image(7)).save()
    def test_check(self):
        usr = User.objects.filter(username='test').first()
        self.assertIsNotNone(usr)
        post = Post.objects.first()
        self.assertIsNotNone(post)
        wish = Wanted.objects.first()
        self.assertIsNotNone(wish)
        self.assertEquals(usr.username, post.owner.username, wish.owner.username)
        c1 = Post.objects.all().count()
        c2 = Wanted.objects.all().count()
        self.assertIs(c1, 4)
        self.assertIs(c2, 3)
        post1 = Post.objects.all().first()
        post2 = Post.objects.all().last()
        self.assertIsNot(post1, post2)
        want1 = Wanted.objects.all().first()
        want2 = Wanted.objects.all().last()
        self.assertIsNot(want1, want2)
        response1 = self.client.get(reverse('index'))
        self.assertIs(response1.status_code, 200)
        response2 = self.client.get(reverse('signup'))
        self.assertIs(response2.status_code, 200)
        res3 = self.client.get(reverse('signin'))
        self.assertIs(res3.status_code, 200)
        self.client.force_login(usr)
        res4 = self.client.get(reverse('top'))
        self.assertIs(res4.status_code, 200)
        self.assertContains(res4, 'Add new cloth')
        self.assertContains(res4, 'detail')
        for n in range(1, 4):
            self.assertContains(res4, 'test{}'.format(n))
        for n in range(1, 4):
            res5 = self.client.get('/clothes/detail/{}'.format(n))
            self.assertIs(res5.status_code, 200)
            self.assertContains(res5, 'test{}'.format(n))
            self.assertContains(res5, 'delete')
            self.assertContains(res5, 'edit')
        res6 = self.client.get(reverse('post'))
        self.assertIs(res6.status_code, 200)
        self.assertContains(res6, 'Add')
        for n in range(1, 4):
            res7 = self.client.get('/clothes/edit/{}'.format(n))
            self.assertIs(res7.status_code, 200)
            self.assertContains(res7, 'test{}'.format(n))
            self.assertContains(res7, 'edit')
        for n in range(1, 4):
            res8 = self.client.get('/clothes/delete/{}'.format(n))
            self.assertIs(res8.status_code, 200)
            self.assertContains(res8, 'test{}'.format(n))
            self.assertContains(res8, 'delete')
        res8 = self.client.get(reverse('search'))
        self.assertIs(res8.status_code, 200)
        self.assertContains(res8, 'search')
        res9 = self.client.get(reverse('wishlist'))
        self.assertIs(res9.status_code, 200)
        self.assertContains(res9, 'Add WishList')
        for n in range(1, 3):
            self.assertContains(res9, 'test{}'.format(n))
            self.assertContains(res9, 'detail')
        res10 = self.client.get(reverse('wishlist_add'))
        self.assertIs(res10.status_code, 200)
        self.assertContains(res10, 'add')
        for n in range(1, 3):
            res11 = self.client.get('/clothes/wishlist_edit/{}'.format(n))
            self.assertIs(res11.status_code, 200)
            self.assertContains(res11, 'test{}'.format(n))
            self.assertContains(res11, 'edit')
        for n in range(1, 3):
            res12 = self.client.get('/clothes/wishlist_delete/{}'.format(n))
            self.assertIs(res12.status_code, 200)
            self.assertContains(res12, 'test{}'.format(n))
            self.assertContains(res12, 'delete')
        for n in range(1, 3):
            res13 = self.client.get('/clothes/wishlist_detail/{}'.format(n))
            self.assertIs(res13.status_code, 200)
            self.assertContains(res13, 'test{}'.format(n))
            self.assertContains(res13, 'delete')
            self.assertContains(res13, 'edit')

class NameSearchFormTest(TestCase):
    def test_form(self):
        data = {"search":"test"}
        form = NameSearchForm(data)
        self.assertTrue(form.is_valid())

class UserCreateFormTest(TestCase):
    def test_form(self):
        data = {
            "username":"test",
            "password1":"kimuson8976",
            "password2":"kimuson8976"
        }
        form = UserCreateForm(data)
        print(form.errors)
        self.assertTrue(form.is_valid())

class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        usr= cls.create_user()
    @classmethod
    def create_user(cls):
        User(username="test", password="test", is_staff=True, is_active=True).save()
        usr = User.objects.filter(username='test').first()
        return(usr)
    def test_form(self):
        usr = User.objects.filter(username='test').first()
        data = {
            "owner":usr,
            "cloth_name":"test1",
            "item_info":1,
            "brand_name":"test1",
            "season":"test1",
            "cloth_size":"test1",
            "material":"test1",
            "price":1,
            "buying_place":"test1",
            "buying_date":datetime.date.today(),
        }
        img_dict = get_post_image_dict()
        form = PostForm(data, img_dict)
        print(form.errors)
        self.assertTrue(form.is_valid())

class WantedFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        usr= cls.create_user()
    @classmethod
    def create_user(cls):
        User(username="test", password="test", is_staff=True, is_active=True).save()
        usr = User.objects.filter(username='test').first()
        return(usr)
    def test_form(self):
        usr = User.objects.filter(username='test').first()
        data = {
            "owner":usr,
            "wanted_cloth_name":"test",
            "wanted_brand_name":"test",
            "wanted_season":"test",
            "wanted_price":1,
            "priority":1
        }
        img_dict = get_wanted_image_dict()
        form = WantedForm(data, img_dict)
        print(form.errors)
        self.assertTrue(form.is_valid())

class LoginFormTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='kimuson9877')
    def LoginFormTestNameError(self):
        data = {
            "username": "error",
            "password": "kimuson9877"
        }
        form = LoginForm(data)
        self.assertFalse(form.is_valid())
    def LoginFormTestPassError(self):
        data = {
            "username": "test",
            "password": "error"
        }
        form = LoginForm(data)
        self.assertFalse(form.is_valid())
    def LoginFormTrue(self):
        data = {
            "username": "test",
            "password": "kimuson9877"
        }
        form = LoginForm(data)
        print(form.errors)
        self.assertTrue(form.is_valid())

class PostClothesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        usr= cls.create_user()
    @classmethod
    def create_user(cls):
        User(username="test", password="test", is_staff=True, is_active=True).save()
        usr = User.objects.filter(username='test').first()
        return(usr)
    def test_cloth_post(self):
        usr = User.objects.filter(username='test').first()
        self.client.force_login(usr)
        data = {
            "owner":usr,
            "cloth_name":"test1",
            "item_info":1,
            "brand_name":"test1",
            "season":"test1",
            "cloth_size":"test1",
            "material":"test1",
            "price":1,
            "buying_place":"test1",
            "buying_date":datetime.date.today(),
        }
        img_dict = get_post_image_dict()
        data = data | img_dict
        response = self.client.post(reverse('post'), data)
        self.assertEqual(response.status_code, 302)
        delete_response = self.client.delete('/clothes/delete/1', data)
        self.assertEqual(delete_response.status_code, 200)

class PostWishListTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        usr= cls.create_user()
    @classmethod
    def create_user(cls):
        User(username="test", password="test", is_staff=True, is_active=True).save()
        usr = User.objects.filter(username='test').first()
        return(usr)
    def test_wishlist_post(self):
        usr = User.objects.filter(username='test').first()
        data = {
            "owner":usr,
            "wanted_cloth_name":"test",
            "wanted_brand_name":"test",
            "wanted_season":"test",
            "wanted_price":1,
            "priority":1
        }
        img_dict = get_wanted_image_dict()
        data = data | img_dict
        response = self.client.post(reverse('wishlist_add'), data)
        self.assertEqual(response.status_code, 302)
        delete_response = self.client.delete('/clothes/wishlist_delete/1', data)
        self.assertEqual(delete_response.status_code, 302)
