from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Article, Investigator


def user_args():
    return dict(username='TESTER', email='test@test.us', password='secret')


def test_user():
    return get_user_model().objects.create_user(**user_args())


class ArticleDataTest(TestCase):

    def setUp(self):
        self.user = test_user()
        self.investigator = Investigator.objects.create(user=self.user, bio='single tester')
        self.article1 = dict(investigator=self.investigator, title='Doc Title 1', body='Doc Body 1')
        self.article2 = dict(investigator=self.investigator, title='Doc Title 2', body='Doc Body 2')

    def test_add_test(self):
        self.assertEqual(len(Article.objects.all()), 0)
        Article.objects.create(**self.article1)
        x = Article.objects.get(pk=1)
        self.assertEqual(x.title, self.article1['title'])
        self.assertEqual(len(Article.objects.all()), 1)

    def test_test_edit(self):
        Article.objects.create(**self.article1)
        x = Article.objects.get(pk=1)
        x.title = self.article2['title']
        x.body = self.article2['body']
        x.save()
        self.assertEqual(x.title, self.article2['title'])
        self.assertEqual(x.body, self.article2['body'])
        self.assertEqual(len(Article.objects.all()), 1)

    def test_test_delete(self):
        Article.objects.create(**self.article1)
        b = Article.objects.get(pk=1)
        b.delete()
        self.assertEqual(len(Article.objects.all()), 0)


class ArticleViewsTest(TestCase):

    def login(self):
        response = self.client.login(username=self.user.username,  password=user_args()['password'])
        self.assertEqual(response, True)

    def setUp(self):
        self.user = test_user()
        self.investigator = Investigator.objects.create(user=self.user, bio='single tester')
        self.article1 = dict(investigator=self.investigator, title='Doc Title 1', body='Doc Body 1')
        self.article2 = dict(investigator=self.investigator, title='Doc Title 2', body='Doc Body 2')

    def test_article_list_view(self):
        self.assertEqual(reverse('article_list'), '/article/')
        Article.objects.create(**self.article1)
        Article.objects.create(**self.article2)
        response = self.client.get('/article/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_list.html')
        self.assertTemplateUsed(response, 'theme.html')
        self.assertContains(response, '<tr>', count=3)

    def test_article_detail_view(self):
        Article.objects.create(**self.article1)
        self.assertEqual(reverse('article_detail', args='1'), '/article/1')
        self.assertEqual(reverse('article_detail', args='2'), '/article/2')
        response = self.client.get(reverse('article_detail', args='1'))
        self.assertContains(response, 'body')

    def test_article_add_view(self):

        # Add without Login
        response = self.client.post(reverse('article_add'), self.article1)
        response = self.client.post(reverse('article_add'), self.article2)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/article/add')

        # Login to add
        self.login()
        response = self.client.post(reverse('article_add'), self.article1)
        a = dict(investigator=self.investigator, title='Doc Title 2', body='Doc Body 2')
        response = self.client.post(reverse('article_add'), a)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(len(Article.objects.all()), 2)

    def test_article_edit_view(self):

        # Edit without Login
        response = Article.objects.create(**self.article1)
        response = self.client.post(reverse('article_edit', args='1'), self.article2)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/article/1/')

        # Login to edit
        self.login()
        response = self.client.post('/article/1/', self.article2)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        article = Article.objects.get(pk=1)
        self.assertEqual(article.title, self.article2['title'])
        self.assertEqual(article.body, self.article2['body'])

    def test_article_delete_view(self):
        self.login()
        Article.objects.create(**self.article1)
        self.assertEqual(reverse('article_delete', args='1'), '/article/1/delete')
        response = self.client.post('/article/1/delete')
        self.assertEqual(len(Article.objects.all()), 0)


class InvestigatorDataTest(TestCase):

    def setUp(self):
        self.user = test_user()
        self.investigator = dict(user=self.user, bio='single tester')

    def test_add_test(self):
        self.assertEqual(len(Investigator.objects.all()), 0)
        Investigator.objects.create(**self.investigator)
        x = Investigator.objects.get(pk=1)
        self.assertEqual(x.user.username, self.investigator['user'].username)
        self.assertEqual(x.bio, self.investigator['bio'])
        self.assertEqual(len(Investigator.objects.all()), 1)

    def test_user_edit(self):
        user = User.objects.get(pk=1)
        user.first_name = 'First'
        user.last_name = 'Last'
        user.email = 'user@a.us'
        user.save()
        user = User.objects.get(pk=1)
        self.assertEqual(user.email, 'user@a.us')

    def test_edit(self):
        Investigator.objects.create(**self.investigator)
        x = Investigator.objects.get(pk=1)
        x.bio = 'new tester'
        x.save()
        self.assertEqual(x.user.username, self.investigator['user'].username)
        self.assertEqual(x.bio, 'new tester')
        self.assertEqual(len(Investigator.objects.all()), 1)

    def test_delete(self):
        Investigator.objects.create(**self.investigator)
        b = Investigator.objects.get(pk=1)
        b.delete()
        self.assertEqual(len(Investigator.objects.all()), 0)


class InvestigatorViewsTest(TestCase):

    def login(self):
        username = self.user.username
        password = user_args()['password']
        response = self.client.login(username=username, password=password)
        self.assertEqual(response, True)

    def setUp(self):
        self.user = test_user()
        self.investigator = dict(user=self.user, bio='single tester')
        self.investigator2 = dict(user=self.user, bio='new tester')

    def test_investigator_list_view(self):
        self.assertEqual(reverse('investigator_list'), '/investigator/')
        Investigator.objects.create(**self.investigator)
        response = self.client.get('/investigator/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'investigator_list.html')
        self.assertTemplateUsed(response, 'theme.html')
        self.assertContains(response, '<tr>', count=2)

    def test_investigator_detail_view(self):
        Investigator.objects.create(**self.investigator)
        self.assertEqual(reverse('investigator_detail', args='1'), '/investigator/1')
        response = self.client.get(reverse('investigator_detail', args='1'))
        self.assertContains(response, 'body')

    def test_investigator_add_view(self):
        # Login to create Investigator
        self.login()
        response = self.client.get('/investigator/home')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/investigator/1')
        self.assertEqual(len(Investigator.objects.all()), 1)

    def test_investigator_home(self):
        # Annonymous should show Articles
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'investigator/home')
        response = self.client.get('/investigator/home')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/article/')
        self.assertEqual(len(Investigator.objects.all()), 0)

    def test_user_edit_view(self):
        # Edit without Login
        user_args = dict(first_name='First', last_name='Last', email='user@a.us', username='TESTER', password='secret')
        response = self.client.post(reverse('user_edit', args='1'), user_args)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/accounts/1/')
        self.assertEqual(User.objects.get(pk=1).email, 'test@test.us')

        # Login to edit
        self.login()
        response = self.client.post('/accounts/1/', user_args)
        self.assertEqual(User.objects.get(pk=1).email, 'user@a.us')

    def test_investigator_edit_view(self):
        # Edit without Login
        response = Investigator.objects.create(**self.investigator)
        response = self.client.post(reverse('investigator_edit', args='1'), self.investigator)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/investigator/1/')

        # Login to edit
        self.login()
        response = self.client.post('/investigator/1/', self.investigator2)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        investigator = Investigator.objects.get(pk=1)
        self.assertEqual(investigator.bio, self.investigator2['bio'])

    def test_investigator_delete_view(self):
        self.login()
        Investigator.objects.create(**self.investigator)
        self.assertEqual(reverse('investigator_delete', args='1'), '/investigator/1/delete')
        response = self.client.post('/investigator/1/delete')
        self.assertEqual(len(Investigator.objects.all()), 0)
