from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from..models import ListTask, Task


User = get_user_model()

class TaskViewSetTest(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username='Test Name',
            password='123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_return_the_user_list(self):
        list_task = ListTask.objects.create(
            title='Test List',
            user=self.user
        )

        url = reverse('task:list-task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_list_in_api(self):
        data = {
            "title": "Test List",
            "description": "Creating a list and testing the user"
        }

        url = reverse('task:list-task-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_edit_the_corresponding_user_task(self):
        list_task = ListTask.objects.create(
            title='Test List',
            user=self.user
        )
        Task.objects.create(
            name='Test Task',
            list_task=list_task
        )

        data = {
            "name": "Name Changed"
        }

        url = reverse('task:task-detail', kwargs={"pk": 1})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_reorder_tasks_in_moved_to_back(self):
        list_task = ListTask.objects.create(
            title='Test List',
            user=self.user
        )
        task1 = Task.objects.create(
            name='Task 1',
            list_task=list_task
        )
        task2 = Task.objects.create(
            name='Task 2',
            list_task=list_task
        )
        task3 = Task.objects.create(
            name='Task 3',
            list_task=list_task
        )
        self.assertEqual(task1.order, 1)
        self.assertEqual(task2.order, 2)
        self.assertEqual(task3.order, 3)

        data = {
            "task_id": 2,
            "new_order": 1
        }

        url = reverse('task:task-reorder')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task reordered successfully', str(response.json()))

    def test_reorder_tasks_in_moved_forward(self):
        list_task = ListTask.objects.create(
            title='Test List',
            user=self.user
        )
        task1 = Task.objects.create(
            name='Task 1',
            list_task=list_task
        )
        task2 = Task.objects.create(
            name='Task 2',
            list_task=list_task
        )
        task3 = Task.objects.create(
            name='Task 3',
            list_task=list_task
        )
        self.assertEqual(task1.order, 1)
        self.assertEqual(task2.order, 2)
        self.assertEqual(task3.order, 3)

        data = {
            "task_id": 1,
            "new_order": 2
        }

        url = reverse('task:task-reorder')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task reordered successfully', str(response.json()))

    def test_reorder_task_not_exist(self):
        data = {
            "task_id": 1,
            "new_order": 2
        }

        url = reverse('task:task-reorder')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Task not found', str(response.json()))

    def test_reorder_task_already_in_position(self):
        list_task = ListTask.objects.create(
            title='Test List',
            user=self.user
        )
        task1 = Task.objects.create(
            name='Task 1',
            list_task=list_task
        )
        task2 = Task.objects.create(
            name='Task 2',
            list_task=list_task
        )
        task3 = Task.objects.create(
            name='Task 3',
            list_task=list_task
        )
        self.assertEqual(task1.order, 1)
        self.assertEqual(task2.order, 2)
        self.assertEqual(task3.order, 3)

        data = {
            "task_id": 2,
            "new_order": 2
        }

        url = reverse('task:task-reorder')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task already in position', str(response.json()))