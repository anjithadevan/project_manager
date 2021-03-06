from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from projects.models import Project, LogActualHourEdit, Tag


class DashboardTestCase(TestCase):

    fixtures = ['projects/fixtures/initial.json']

    def setUp(self):
        super().setUp()

        username, password = 'Thorgate', 'thorgate123'
        User.objects.create_user(username=username, email='info@throgate.eu', password=password)

        self.authenticated_client = Client()
        self.authenticated_client.login(username=username, password=password)

    def test_dashboard_requires_authentication(self):

        # Anonymous users can't see the dashboard

        client = Client()
        response = client.get('/dashboard/')
        self.assertRedirects(response, '/login/?next=/dashboard/')

        # Authenticated users can see the dashboard

        response = self.authenticated_client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_projects_on_dashboard(self):

        # There are 3 projects on the dashboard (loaded from the fixtures)

        response = self.authenticated_client.get('/dashboard/')
        projects = response.context['projects']
        self.assertEqual(len(projects), 3)

    def test_edit_project(self):

        self.project = Project.objects.latest('id')
        update_url = reverse('project-update', args=(self.project.pk, self.project.title))
        response = self.authenticated_client.post(update_url, {}, content_type='application/json')
        self.assertEqual(response.status_code, 200)


class ProjectsTestCase(TestCase):
    fixtures = ['projects/fixtures/initial.json']

    def setUp(self):
        super().setUp()

        self.projects = Project.objects.order_by('id')

    def test_project_has_ended(self):

        # 2 of the projects have ended
        self.assertListEqual([p.has_ended for p in self.projects], [True, True, False])

    def test_project_is_over_budget(self):

        # 1 of the projects is over budget
        self.assertListEqual([p.is_over_budget for p in self.projects], [True, False, False])

    def test_total_estimated_hours(self):

        self.assertListEqual([p.total_estimated_hours for p in self.projects], [690, 170, 40])

    def test_total_actual_hours(self):

        self.assertListEqual([p.total_actual_hours for p in self.projects], [739, 60, 5])


class TagTestCase(TestCase):

    def setUp(self):
        super().setUp()

    def test_creation(self):
        tags_count_initial = Tag.objects.all().count()
        Tag.objects.create(name="test")
        tags_count_now = Tag.objects.all()
        self.assertNotEqual(tags_count_initial, tags_count_now.count())
        Tag.objects.all().delete()
        self.assertEqual(tags_count_initial, tags_count_now.count())