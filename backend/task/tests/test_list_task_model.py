from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import ListTask, Task


User = get_user_model()

class TestModelList(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.list_task = ListTask.objects.create(
            title='Test List',
            description='A test list',
            user=self.user
        )
    
    def test_create_list(self):
        self.assertEqual(ListTask.objects.count(), 1)
        self.assertEqual('Test List', self.list_task.__str__())

    def test_list_update_completion(self):
        total = self.list_task.tasks.count()
        self.assertEqual(self.list_task.completion_percentage, total)

    def test_completion_percentage_task_in_list(self):
        Task.objects.create(
            name='Task 1',
            is_completed=True,
            list_task=self.list_task
        )
        Task.objects.create(
            name='Task 2',
            is_completed=False,
            list_task=self.list_task
        )
        self.assertEqual(self.list_task.completion_percentage, 50)

    def test_name_in_task(self):
        task = Task.objects.create(name='Test', list_task=self.list_task)
        self.assertEqual('Test', task.__str__())

    def test_delete_task_reoder(self):
        task1 = Task.objects.create(name='Task 1', list_task=self.list_task)
        task2 = Task.objects.create(name='Task 2', list_task=self.list_task)
        task3 = Task.objects.create(name='Task 3', list_task=self.list_task)

        task2.delete()
        task3.refresh_from_db()

        self.assertEqual(task3.order, 2)