---
layout: post
comments: true
title:  "Django Unit Testing"
date:   2018-05-03
categories: [python, django, unit-testing]
author: Anjaneyulu
---
### Why testing is important ?
Testing is very important to any web appication. Because the application may contain errors that are not inteded and it may cause some serious problems. So, we need to test everything to make sure that it's working as intended.

### Types of Testing
In general testing can be done in two ways 1. Manual testing 2. Automated Testing

* #### Manual Testing:
It needs a human resource to test the application and we call the resource as Tester. Tester will test the appication manually by checking each and every functionality that the web appication provides.
Manual testing is a time cosuming process so it will take more time and some times there is possibility of missing some functionality to test. This will result in bugs. So, manual testing is not accurate.

* #### Automated Testing:
In this approach we automate tests for each and every functionality of the web appication. This approach is 100% accurate and it takes less time to test the web appication functionalities and we don't need a human intervention.

### Unit Testing
* Let's consider a large web applications like Amazon, Flipcart, etc. These are very complex applications. Testing the application as whole is difficult task and it may not yield best results. So, we divide the application into simpler modules and modules to sub modules and so on. We call the sub module as Unit and it will not further devided.
We test these units individually by writing the automated tests for each so, it will produce accurate test results.


### Django Unit Testing Process

Each django unit test comprises of 3 methods. 1. `setUp`, 2. `test_<test_name>` and 3.`tearDown`.
When we run the test using command `python manage.py test` test runner will create a empty test database with required migrations. It will look for the tests in the files whose name starts with test and finds the all tests. The test runner will take the each test case and runs it. Whenever the test is running first it will call "setUp" method which is used to create basic requirements to run the test. After, it will run the test and then the method "`tearDown`" will be called. "`tearDown`" is used to destroy the data created by the "`setUp`" method. Django unit testing has a automated mechanism to remove it. But, in some cases we need to do it manually.

Note: Take separate class for each test. Writing multiple tests in the same class will slow down the tests run time.


### Advantages of writing unit tests in Django
Django is comprised of different modules like models, forms, views, templates, etc. When we develop an application we devide it into functionalities and develop them independently. So, we write unit test to test the funcitonality whether its working as we expected or not. Ofcourse, it will work as we expected. We develop all other functionalities so, apperently the applicaiton will become complex. In development process we definitely have a dependent funcitonalities. After completion of the application we make it available to the world.
As we follow agile development the changes in the functionalities are infly. So, changing in one functionality will result error in other functionality. In such cases the unit test's helps us to fix the bugs that produced by latest changes. So, it's vital to write unit tests in our django applications.

### Best practices for Django Unit Testing
1. Each test case should have to test a single functionality
2. We have to keep in simple and there should not be a dependency between testcases
3. Run the `tests` every time you pull the code or before pushing the code.
4. we can use the naming convension `tests.py` or we can create directory named `tests` like below for better project structure.
   ```bash
   └── app_name
    └── tests
        ├── __init__.py
        ├── test_forms.py
        ├── test_models.py
        └── test_views.py
   ```

### Modules needs to be tested in Django
Let's see example test cases how we can write for modules like models, forms, views, template tags, etc.
* #### Writing tests for Models

models.py

```python
from django.db import models
from django.contrib.auth.models import AbscractUser

class User(AbstractUser):
    AUTHOR = 1
    PUBLISHER = 2
  USER_TYPES = (
    (AUTHOR, 'Author'),
    (PUBLISHER, 'Publisher'),
  )
    user_type = models.CharField(choices=USER_TYPES)
    no_of_books = models.IntegerField(default=0)

    @classmethod
    def get_authors(cls,):
        return cls.objects.filter(uset_type=cls.AUTHOR)

    def can_write_books(self):
        return self.user_type == self.AUTHOR
```

tests.py

```python
from django.test import TestCase
from .models import User

class UserTestCase(TestCase):

    def setUp(self):
        self.author = User.objects.create(
          username='author@test.com',
          email='author@test.com',
          user_type=User.AUTHOR
        )
        self.publisher = User.objects.create(
          username='publisher@test.com',
          email='publisher@test.com',
          user_type=User.AUTHOR
        )

    def test_get_authors(self):
      self.assertEqual(User.get_authors(), 1)

    def test_can_write_books(self):
      self.assertTrue(self.author.can_write_books())
      self.assertFalse(self.publisher.can_write_books())

```

* #### Writing tests for Forms

forms.py

```python
from django import forms

class RegistrationForm(forms.Form):

  username = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput())
  confirm = forms.CharField(widget=forms.PasswordInput())

  def clean(self):
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')
    confirm = self.cleaned_data.get('confirm')
    if confirm != password:
      raise forms.ValidationError({
        'confirm': 'Passwords mismatched'
      })
    return self.cleaned_data

```
tests.py
```python
from django.test import TestCase
from .forms import RegistrationForm


class TestRegistrationForm(TestCase):
  
  def test_registration_form(self):
    # test invalid data
    invalid_data = {
      "username": "user@test.com",
      "password": "secret",
      "confirm": "not secret"
    }
    form = RegistrationForm(data=invalid_data)
    form.is_valid()
    self.assertTrue(form.errors)

    # test valid data
    valid_data = {
      "username": "user@test.com",
      "password": "secret",
      "confirm": "secret"
    }
    form = RegistrationForm(data=valid_data)
    form.is_valid()
    self.assertFalse(form.errors)

```

* #### Writing tests for Views

views.py

```python
from django.views.generic import FormView
from django.http import JsonResponse
from .forms import RegistrationForm

class UserRegistrationView(FormView):
  form_class = RegistrationForm

  def form_valid(self, form):
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    User.objects.create_user(username, password=password)
    res_data = {
      'error': False,
      'message': 'Success, Please login'
    }
    return JsonResponse(res_data)

  def form_invalid(self, form):
    res_data = {
      'error': True,
      'errors': form.errors
    }
    return JsonResponse(res_data)

```

urls.py

```python
from django.urls import path

from . import views

urlpatterns = [
  path('registration/',
       views.UserRegistrationView.as_view(), name='register'
  )
]

```

tests.py

```python
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class TestUserRegistrationView(TestCase):

  def setUp(self):
    self.client = Client()

  def test_registration(self):
    url = reverse('register')
    
    # test req method GET
    response = self.client.get(url)
    self.assertEqual(response.status, 200)

    # test req method POST with empty data
    response = self.client.post(url, {})
    self.assertEqual(response.status, 200)
    exp_data = {
      'error': True,
      'errors': {
        'username': 'This field is required',
        'password': 'This field is required',
        'confirm': 'This field is required',
      }
    }
    self.asssertEqual(exp_data, response.json())
    
    # test req method POST with invalid data
    req_data = {
      'username': 'user@test.com',
      'password': 'secret',
      'confirm': 'secret1',
    }
    response = self.client.post(url, req_data)
    self.assertEqual(response.status, 200)
    exp_data = {
      'error': True,
      'errors': {
        'confirm': 'Passwords mismatched'
      }
    }
    self.asssertEqual(exp_data, response.json())

    # test req method POST with valid data
    req_data = {
      'username': 'user@test.com',
      'password': 'secret',
      'confirm': 'secret',
    }
    response = self.client.post(url, req_data)
    self.assertEqual(response.status, 200)
    exp_data = {
      'error': False,
      'message': 'Success, Please login'
    }
    self.asssertEqual(exp_data, response.json())
    self.assertEqual(User.objects.count(), 1)
```


* #### Writing tests for Template tags

See how to write custom template tags in [django official docs](https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/){:target="_blank"}

custom_template_tags.py

```python
from django import template

register = template.Library()


@register.filter(is_safe=True)
def add_xx(value):
    return '%sxx' % value
```

tests.py

```python
from django.test import TestCase
from django.template import Template


class TestAddXX(TestCase):

  def test_add_xx(self):
    template = Template('''
      {{ "{%" }} load custom_template_tags %}
      {{ "{{" }} "django_2."{{ "|" }}add_xx }}
    ''')
    rendered_text = template.render()
    self.assertIn("django_2.xx", rendered_text)
```

### Finding code coverage with "coverage"
Now, it's time to find how much code is executing when test cases are running. If we have written all possible tests for the application then the code coverage will be 100% otherwise it will show us the missing lines of code. To do it we have to install the pip package "coverage"

Install coverage using pip
```bash
pip install coverage
```

Using coverage package

```bash
coverage run --source=app1,app2 ---omit=*/migrations/*  manage.py test

```

  Above command will executes the tests and stores the test results.

  To know the results run the below command
```bash
coverage report -m
```

Above command will return results like below(example output).
```bash
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
app1/views.py                20      4    80%   33-35, 39
app1/models.py               20      4    80%   35-41, 57
app1/templatetags/ctags.py   56      6    89%   17-23
-------------------------------------------------------
TOTAL                        76     10    87%
```

### References:

[http://django-testing-docs.readthedocs.io/en/latest/basic_doctests.html](http://django-testing-docs.readthedocs.io/en/latest/basic_doctests.html){:target="_blank"}
[https://docs.djangoproject.com/en/2.0/topics/testing/overview/](https://docs.djangoproject.com/en/2.0/topics/testing/overview/){:target="_blank"}
