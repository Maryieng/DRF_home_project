from rest_framework.test import APITestCase, APIClient

from lms.models import Well, Lesson, Subscription
from users.models import User
from django.urls import reverse
from rest_framework import status


class LessonTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='teatuser@gmail.ru', is_superuser=True, is_staff=True)
        self.user.set_password('testtesttest')
        self.client.force_authenticate(user=self.user)
        self.well = Well.objects.create(title='test')
        self.lesson = Lesson.objects.create(title='test', well=self.well,
                                            video_link='https://www.youtube.com/123')

    def test_create_lesson(self):
        data = {"title": "test", "description": "test", "video_link": "https://www.youtube.com/watch"}
        response = self.client.post('/lesson/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'id': 2, 'title': 'test', 'description': 'test', 'preview': None,
                                           'video_link': 'https://www.youtube.com/watch', 'well': None, 'owner': 1})

    def test_list_lesson(self):
        Lesson.objects.create(title="list", description="list")
        response = self.client.get('/lesson/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_lesson(self):
        response = self.client.get(reverse('lms:lesson_view', kwargs={'pk': self.lesson.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        data = {"title": "test", "description": "test", "video_link": "https://www.youtube.com/123"}
        response = self.client.patch(reverse('lms:lesson_update', kwargs={'pk': self.lesson.pk}), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        response = self.client.delete(reverse('lms:lesson_delete', kwargs={'pk': self.lesson.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_validator(self):
        data = {"title": "test", "description": "test", "video_link": "https://www.test.com/54321"}
        response = self.client.post(reverse('lms:lesson_create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Ссылки на сторонние образовательные платформы или личные сайты — запрещены']})


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="kass.o@yandex.ru")
        self.user.set_password('12345')
        self.client.force_authenticate(user=self.user)
        self.well = Well.objects.create(title="test", owner=self.user)
        self.data = {"user": self.user.pk, "well": self.well.pk}

    def test_subscribe(self):
        url = reverse('lms:subscribe', args=(self.well.pk,))
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Подписка добавлена'})

    def test_unsubscribe(self):
        url = reverse('lms:subscribe', args=(self.well.pk,))
        Subscription.objects.create(well=self.well, user=self.user)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Подписка удалена'})
