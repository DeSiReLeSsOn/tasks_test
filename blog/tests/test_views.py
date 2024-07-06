import pytest
from rest_framework.reverse import reverse
from conftest import test_user, test_user_wrong, test_post, test_staff_user  
from rest_framework.test import APIClient
from blog.models import Post
from blog.serializers import PostSerializer
from rest_framework import status


@pytest.mark.django_db
def test_post_list_view_get_anonymous():
    client = APIClient()
    response = client.get(reverse('posts'))
    assert response.status_code == status.HTTP_200_OK

    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    assert response.data == serializer.data


@pytest.mark.django_db
def test_post_list_authenticated_client(test_user):
    client = APIClient()
    client.force_authenticate(user=test_user)
    response = client.get(reverse('posts'))
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data 


@pytest.mark.django_db
def test_post_list_view_post_authenticated(test_user):
    client = APIClient()
    client.force_authenticate(user=test_user)
    data = {
        'author': test_user.pk,
        'title': 'second post',
        'text': 'text2', 
        'is_published': False
    }
    response = client.post(reverse('posts'), data, format='json')
    print(Post.objects.all())

    assert response.status_code == status.HTTP_201_CREATED
    
    assert Post.objects.count() == 2


@pytest.mark.django_db
def test_post_list_view_post_anonymous():
    client = APIClient()
    data = {
        'title': 'second post wrong',
        'text': 'text2', 
        'is_published': False
    }

    response = client.post(reverse('posts'), data, format='json')

    assert response.status_code == 403
    

    

@pytest.mark.django_db
def test_post_detail_view_get_anonymous(test_post):
    client = APIClient()
    response = client.get(reverse('post-detail', kwargs={'pk': test_post.pk})) 

    
    serializer = PostSerializer(test_post)

    assert response.status_code == status.HTTP_200_OK 
    assert response.data == serializer.data


@pytest.mark.django_db
def test_post_detail_view_get_authenticated(test_post, test_user):
    client = APIClient()
    client.force_authenticate(user=test_user)

    response = client.get(reverse('post-detail', kwargs={'pk': test_post.pk})) 

    serializer = PostSerializer(test_post)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data
    



@pytest.mark.django_db
def test_post_detail_view_get_not_found():
    client = APIClient()
    response = client.get(reverse('post-detail', kwargs={'pk': 999}))
    assert response.status_code == status.HTTP_404_NOT_FOUND 



@pytest.mark.django_db
def test_post_detail_view_put_authenticated_author(test_user, test_post):
    client = APIClient()
    client.force_authenticate(user=test_user)
    data = {
        'author': test_user.pk,
        'title': 'refresh title',
        'text': 'refresh text'
    }
    response = client.put(reverse('post-detail', kwargs={'pk': test_post.pk}), data, format='json')
    assert response.status_code == status.HTTP_200_OK

    test_post.refresh_from_db()
    assert test_post.title == 'refresh title'
    assert test_post.text == 'refresh text' 



@pytest.mark.django_db
def test_post_detail_view_put_authenticated_not_author(test_post, test_user_wrong):
    client = APIClient()
    client.force_authenticate(user=test_user_wrong)
    data = {
        'author': test_user_wrong.pk,
        'title': 'Обновленный заголовок',
        'content': 'Обновленное содержание'
    }
    response = client.put(reverse('post-detail', kwargs={'pk': test_post.pk}), data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN 


@pytest.mark.django_db
def test_post_detail_view_put_staff(test_post, test_staff_user):
    client = APIClient()
    client.force_authenticate(user=test_staff_user)
    data = {
        'author': test_staff_user.pk,
        'title': 'Обновленный заголовок',
        'text': 'Обновленное содержание'
    }
    response = client.put(reverse('post-detail', kwargs={'pk': test_post.pk}), data, format='json')
    assert response.status_code == status.HTTP_200_OK

    test_post.refresh_from_db()
    assert test_post.title == 'Обновленный заголовок'
    assert test_post.text == 'Обновленное содержание'



@pytest.mark.django_db
def test_post_detail_view_delete_authenticated_author(test_post, test_user):
    client = APIClient()
    client.force_authenticate(user=test_user)
    response = client.delete(reverse('post-detail', kwargs={'pk': test_post.pk}))

    assert response.status_code == status.HTTP_204_NO_CONTENT 

    assert Post.objects.count() == 0 


@pytest.mark.django_db
def test_post_detail_view_delete_authenticated_not_author(test_post, test_user_wrong):
    client = APIClient()
    client.force_authenticate(user=test_user_wrong)
    response = client.delete(reverse('post-detail', kwargs={'pk':test_post.pk}))

    assert response.status_code == status.HTTP_403_FORBIDDEN 


@pytest.mark.django_db
def test_post_detail_view_delete_staff(test_post, test_staff_user):
    client = APIClient()
    client.force_authenticate(user=test_staff_user)
    response = client.delete(reverse('post-detail', kwargs={'pk': test_post.pk}))

    assert response.status_code == status.HTTP_204_NO_CONTENT  


    assert Post.objects.count() == 0 
