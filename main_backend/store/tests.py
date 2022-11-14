"""
Test module for the Store app
The tests in this module doesn't include APIs tests
"""
import shutil
import tempfile
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase, override_settings

from store.models import Category, Album, image_rename, Product

MEDIA_ROOT = tempfile.mkdtemp()


def generate_image(name):
    from PIL import Image
    img = Image.new(mode="RGB", size=(400, 300), color=(209, 123, 193))
    thumb_io = BytesIO()
    img.save(thumb_io, 'JPEG', quality=85)
    image = File(thumb_io, name=name)
    return image


class TestCategoryModel(TestCase):
    """
    Test Class for Category Model in Store app
    """

    def setUp(self) -> None:
        self.UserModel = get_user_model()
        self.user = self.UserModel.objects.create(username='testuser', password='1234', email='abdoo@outlook.com')
        self.data1 = Category.objects.create(name='django', slug='django-test', created_by=self.user)
        self.data2 = Category.objects.create(name='asqlite', slug='asqlite', created_by=self.user)

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_ordering(self):
        categories = Category.objects.all()
        self.assertEqual(str(categories[0]), 'asqlite')

    def test_category_object_name(self):
        """
        Test Category model default object name (reference)
        """
        data = self.data1
        self.assertEqual(str(data), 'django')

    def test_model_url(self):
        """
        Test Category model absolute url
        """
        data = self.data1
        self.assertEqual(data.get_absolute_url, 'django-test')


class TestAlbumModel(TestCase):
    """
    Test Class for Album Model in Store app
    """

    def setUp(self) -> None:
        self.UserModel = get_user_model()
        self.user1 = self.UserModel.objects.create(username='testuser', password='123456789', email='abdoo@outlook.com')
        self.categ1 = Category.objects.create(name='django', slug='django-test', created_by=self.user1)
        self.product = Product.objects.create(category=self.categ1, title='Django project',
                                              slug='django-project', description='This is the main django project',
                                              price=125, created_by=self.user1)
        self.image = generate_image('docker.png')
        self.data1 = Album.objects.create(content_object=self.product, image=self.image,
                                          created_by=self.product.created_by)

    def test_image_url(self):
        """
        Test Category model absolute url
        """
        data = self.data1
        self.assertEqual(data.get_absolute_url, f'/media/{data.image.name}')

    def test_image_rename(self):
        data = self.data1
        self.assertEqual(image_rename(data, 'docker.png'), 'user_1/docker.png')


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestProductModel(TestCase):
    """
    Test Class for Product Model in Store app
    """

    def setUp(self) -> None:
        """
        Set up method has 2 model instance to test.
        """
        self.UserModel = get_user_model()
        # first data instance
        self.user1 = self.UserModel.objects.create(username='testuser', password='123456789', email='abdoo@outlook.com')
        self.categ1 = Category.objects.create(name='django', slug='django-test', created_by=self.user1)
        self.data1 = Product.objects.create(category=self.categ1, title='Django project',
                                            slug='django-project', description='This is the main django project',
                                            price=125, created_by=self.user1)

        self.image = generate_image('docker.png')
        self.image2 = generate_image('docker2.png')
        self.data1.images.create(image=self.image, created_by=self.data1.created_by)
        self.data1.images.create(image=self.image2, created_by=self.data1.created_by)

        # second data instance
        self.user2 = self.UserModel.objects.create(username='testuser2', password='123456789', email='abdoo2@outlook.com')
        self.categ2 = Category.objects.create(name='flask', slug='flask-test', created_by=self.user2)
        self.data2 = Product.objects.create(category=self.categ2, title='Zsqlite project',
                                            slug='zsqlite-project', description='This is the main asqlite project',
                                            price=125, created_by=self.user2)
        self.image3 = generate_image('django.png')
        self.image4 = generate_image('django2.png')
        self.data2.images.create(image=self.image3, created_by=self.data2.created_by)
        self.data2.images.create(image=self.image4, created_by=self.data2.created_by)

    def test_product_model_entry(self):
        """
        Test Product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))

    def test_product_object_name(self):
        """
        Test Product model default object name (reference)
        """
        data = self.data1
        self.assertEqual(str(data), 'Django project')

    def test_product_url(self):
        """
        Test Product model absolute url
        """
        data = self.data1
        self.assertEqual(data.get_absolute_url, 'django-project')

    def test_product_ordering(self):
        products = Product.objects.all()
        self.assertEqual(str(products[0]), 'Zsqlite project')

    def test_thumbnail_url(self):
        data = self.data1
        self.assertEqual(Path(data.get_thumbnail).resolve().parent,
                         Path(f'{settings.MEDIA_URL}thumbnail/user_1/docker_image.png').resolve().parent)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
