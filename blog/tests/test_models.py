import pytest
from django.contrib.auth.models import User
from conftest import test_user, test_post, test_user_wrong
from blog.models import Post


@pytest.mark.django_db
def test_user(test_user):
    assert User.objects.count() == 1
    assert test_user.username == 'test_user'
    assert test_user.email == 'test@gmail.com' 


@pytest.mark.django_db
def test_user_wrong(test_user_wrong):
    assert User.objects.count() == 2
    assert test_user_wrong.username == 'test_user_wrong'
    assert test_user_wrong.email == 'test1@gmail.com'




@pytest.mark.django_db
def test_post_model(test_user, test_post):
    assert Post.objects.count() == 1
    assert test_post.author == test_user
    assert test_post.title == 'test_post'
    assert test_post.text == 'test_post_text'
    assert test_post.is_published is False
    assert str(test_post) == 'test_post'
    