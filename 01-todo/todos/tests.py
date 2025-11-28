from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo

class TodoModelTest(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test TODO",
            description="Test Description",
            status="pending"
        )
    
    def test_create_todo(self):
        """Test creating a TODO"""
        self.assertEqual(self.todo.title, "Test TODO")
        self.assertEqual(self.todo.description, "Test Description")
    
    def test_default_status_is_pending(self):
        """Test that default status is pending"""
        todo = Todo.objects.create(title="New TODO")
        self.assertEqual(todo.status, "pending")
    
    def test_todo_str_returns_title(self):
        """Test that __str__ returns title"""
        self.assertEqual(str(self.todo), "Test TODO")
    
    def test_created_at_is_set(self):
        """Test that created_at is automatically set"""
        self.assertIsNotNone(self.todo.created_at)
    
    def test_updated_at_is_set(self):
        """Test that updated_at is automatically set"""
        self.assertIsNotNone(self.todo.updated_at)


class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
    
    def test_home_page_status_code(self):
        """Test that home page returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_home_page_uses_correct_template(self):
        """Test that home page uses home.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_home_page_extends_base(self):
        """Test that home page extends base.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'base.html')
    
    def test_home_page_has_welcome_message(self):
        """Test that home page has welcome message"""
        response = self.client.get(self.url)
        self.assertContains(response, "Welcome to TODO App")
    
    def test_home_page_has_link_to_todos(self):
        """Test that home page has link to TODOs"""
        response = self.client.get(self.url)
        self.assertContains(response, reverse('todo-list'))


class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
    
    def test_home_page_status_code(self):
        """Test that home page returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_home_page_uses_correct_template(self):
        """Test that home page uses home.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_home_page_extends_base(self):
        """Test that home page extends base.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'base.html')
    
    def test_home_page_has_welcome_message(self):
        """Test that home page has welcome message"""
        response = self.client.get(self.url)
        self.assertContains(response, "Welcome to TODO App")
    
    def test_home_page_has_link_to_todos(self):
        """Test that home page has link to TODOs"""
        response = self.client.get(self.url)
        self.assertContains(response, reverse('todo-list'))


class TodoListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('todo-list')
        self.todo = Todo.objects.create(
            title="Test TODO",
            description="Test Description"
        )
    
    def test_list_view_status_code(self):
        """Test that list view returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_list_view_uses_correct_template(self):
        """Test that list view uses todo_list.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_list.html')
    
    def test_list_view_displays_todos(self):
        """Test that list view displays all TODOs"""
        response = self.client.get(self.url)
        self.assertContains(response, "Test TODO")
    
    def test_list_view_empty_message(self):
        """Test that empty list shows message"""
        Todo.objects.all().delete()
        response = self.client.get(self.url)
        self.assertContains(response, "No TODOs yet")


class TodoCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('todo-create')
    
    def test_create_view_get_status_code(self):
        """Test that GET request returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_create_view_uses_correct_template(self):
        """Test that create view uses todo_form.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
    
    def test_create_todo_post(self):
        """Test creating a TODO via POST"""
        data = {
            'title': 'New TODO',
            'description': 'New Description',
            'status': 'pending'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Todo.objects.filter(title='New TODO').exists())
    
    def test_create_todo_redirect(self):
        """Test that create redirects to list"""
        data = {
            'title': 'New TODO',
            'description': 'New Description',
            'status': 'pending'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('todo-list'))
    
    def test_create_todo_title_required(self):
        """Test that title is required"""
        data = {
            'description': 'No Title',
            'status': 'pending'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        self.assertFalse(Todo.objects.filter(description='No Title').exists())


class TodoEditViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Original Title",
            description="Original Description",
            status="pending"
        )
        self.url = reverse('todo-edit', kwargs={'pk': self.todo.pk})
    
    def test_edit_view_get_status_code(self):
        """Test that GET request returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_edit_view_uses_correct_template(self):
        """Test that edit view uses todo_form.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
    
    def test_edit_todo_post(self):
        """Test updating a TODO via POST"""
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'status': 'completed'
        }
        response = self.client.post(self.url, data)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertEqual(self.todo.status, 'completed')
    
    def test_edit_todo_redirect(self):
        """Test that edit redirects to list"""
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'status': 'completed'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('todo-list'))
    
    def test_edit_nonexistent_todo_404(self):
        """Test that editing non-existent TODO returns 404"""
        url = reverse('todo-edit', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(
            title="TODO to Delete",
            description="Delete Me"
        )
        self.url = reverse('todo-delete', kwargs={'pk': self.todo.pk})
    
    def test_delete_view_get_status_code(self):
        """Test that GET request returns 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_view_uses_correct_template(self):
        """Test that delete view uses todo_confirm_delete.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_confirm_delete.html')
    
    def test_delete_todo_post(self):
        """Test deleting a TODO via POST"""
        response = self.client.post(self.url)
        self.assertFalse(Todo.objects.filter(pk=self.todo.pk).exists())
    
    def test_delete_todo_redirect(self):
        """Test that delete redirects to list"""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('todo-list'))
    
    def test_delete_nonexistent_todo_404(self):
        """Test that deleting non-existent TODO returns 404"""
        url = reverse('todo-delete', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)