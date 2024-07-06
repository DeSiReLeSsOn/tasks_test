import pytest
from django.contrib.auth.models import User
from blog.models import Post


pytestmark = pytest.mark.django_db


@pytest.fixture
def test_user():
    test_user = User.objects.create_user(
        username='test_user',
        email='test@gmail.com',
        password='test_password'
    )
    return test_user


@pytest.fixture
def test_user_wrong():
    test_user_wrong= User.objects.create_user(
        username='test_user_wrong',
        email='test1@gmail.com',
        password='test_password1'
    )
    return test_user_wrong


@pytest.fixture
def test_staff_user():
    user = User.objects.create_user(
        username='test_staff_user',
        password='testpassword',
        is_staff=True
    )
    return user



@pytest.fixture(autouse=True)
def test_post(test_user):
    test_post = Post.objects.create(
        author=test_user,
        title='test_post',
        text='test_post_text',
        is_published=False
    )
    return test_post