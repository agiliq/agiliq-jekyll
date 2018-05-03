---
layout: post
comments: true
title:  "Django Unit Testing"
date:   2018-05-03
categories: [python, django, unit-testing]
author: Anjaneyulu
---
### Why testing is important ?
Testing is very important to any web appication. Because the product may contain errors that are not inteded and it may cause some serious problems to the product/appliation. So, we need to test everything to make sure that it's working as intended.

### Types of Testing
In general testing can be done in two ways 1. Manual testing 2. Automated Testing

* #### Manual Testing:
It needs a human resource to test the application and we call the resource as a Tester. Tester will test the web appication manually by checking each and every functionality that the web appication provides.
Manual testing is a time cosuming process so it will take more time and some times there is possibility of missing some functionality to test. This will result in more bugs. So, manual testing is not accurate.

* #### Automated Testing:
In this approach we automate tests for each and every functionality of the web appication. This approach is 100% accurate and it takes less time to test the web appication functionalities and we don't need a human intervention.

### Unit Testing
* If we consider a large web applications like Amazon, Flipcart, etc. These are very complex applications. Testing the application as whole is difficult task and it may not yield best results. So, we divide the application into simpler modules and modules to sub modules and so on. We call the sub module as Unit and it will not further devided.
We test these units individually by writing the automated tests for each unit and it will produce accurate test results.

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
			raise forms.ValidationError('Passwords mismatched')
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
* #### Writing tests for Template tags

### Finding code coverage with "coverage"
* Test coverage
