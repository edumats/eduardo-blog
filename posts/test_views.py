from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Author, Post, Category


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'tester'
        self.password = 'testuser123'

        # When using create_user(), login is successful
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

        self.author = Author()
        self.author.user = self.user
        self.author.profile_picture = 'profile_images/image_profile.jpg'
        self.author.save()

        self.post1 = Post.objects.create(
            title='Test1',
            description='Testing a post',
            content='<h1>This is a test 1</h1> <p>Testing 1, 2, 3</p>',
            author=self.author,
            featured=True
        )

        self.post2 = Post.objects.create(
            title='Test2',
            description='Testing a post',
            content='<h1>This is a test 2</h1> <p>Testing 1, 2, 3</p>',
            author=self.author,
            featured=True
        )

        self.post3 = Post.objects.create(
            title='Test3',
            description='Testing a post',
            content='<h1>This is a test 3</h1> <p>Testing 1, 2, 3</p>',
            author=self.author,
            featured=True
        )

        self.post4 = Post.objects.create(
            title='Test4',
            description='Testing a post',
            content='<h1>This is a test 4</h1> <p>Testing 1, 2, 3</p>',
            author=self.author,
            featured=True
        )
        self.category1 = Category.objects.create(title='Test Category 1')
        self.category2 = Category.objects.create(title='Test Category 2')
        self.category3 = Category.objects.create(title='Test Category 3')

        self.post1.categories.add(self.category1)
        self.post2.categories.add(self.category2)
        self.post3.categories.add(self.category3)

    def test_index_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_post_list_get(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '../templates/blog.html')

    def test_post_detail_get(self):
        response = self.client.get(reverse('post-detail', args=['test1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '../templates/post.html')

    def test_login_successful(self):
        ''' Checks if client can be authenticated '''
        self.client.login(username=self.username, password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

    def test_post_delete_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('post-delete', args=['test1']))
        # Returning 200 response after login
        # redirects to /accounts/login/?next=/post/test1/delete
        self.assertEqual(response.status_code, 200)

        # Render delete template
        self.assertTemplateUsed(response, '../templates/post_delete_form.html')

    def test_post_delete_POST(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('post-delete', args=['test1']))
        # Gets 302 as the DeleteView redirects to index page
        self.assertEqual(response.status_code, 302)

    def test_post_create_POST(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('post-create'), {
            'title': 'Test5',
            'description': 'Testing a post',
            'content': '<h1>This is a test</h1> <p>Testing 1, 2, 3</p>',
            'author': self.author,
        })
        self.assertEqual(response.status_code, 200)

    def test_search_get(self):
        response = self.client.get(reverse('search'), {'search': 'post1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '../templates/search_results.html')

    def test_category_list_get(self):
        response = self.client.get(reverse('category_list', args=['test_category_1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '../templates/posts_list_by_category.html')
