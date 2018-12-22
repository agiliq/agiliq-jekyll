---
layout: post
comments: true
title:  "When and how to use Django ListView"
date:   2017-12-29 11:36:39+05:30
categories: django
author: akshar
---

### When to use ListView?

Django provides several class based generic views to accomplish common tasks. One among them is ListView.

Most basic class based generic view is TemplateView. We wrote about it in our <a href="http://agiliq.com/blog/2017/12/when-and-how-use-django-templateview/" target="_blank">last post.</a>

ListView **should be used** when you want to present a list of objects in a html page.

ListView **shouldn't be used** when your page has forms and does creation or update of objects. FormView, CreateView and UpdateView are more suitable for working with forms, creation or updation of objects.

TemplateView can achieve everything which ListView can, but ListView has an advantage of avoiding a lot of boilerplate code which would be needed with TemplateView.

Let's write a view using base view **View** and then modify it to use TemplateView and then to use ListView. ListView would help us avoid several lines of code and would also provide better separation of concern.

### Vanilla View

Assume there is a model called Book which looks like:

    class Book(models.Model):
        name = models.CharField(max_length=100)
        author_name = models.CharField(max_length=100)

We want to have a page which shows all the books in the database. View would look like:

	class BookListView(View):

		def get(self, request, *args, **kwargs):
			books = Book.objects.all()
			context = {'books': books}
			return render(request, "book-list.html", context=context)

book-list.html looks like the following:

	{% for book in books %}
	  {{book.name}}
	  <br/>
	{% endfor %}

#### By subclassing TemplateView

	class BookListView(TemplateView):
		template_name = 'book-list.html'

		def get_context_data(self, *args, **kwargs):
			context = super(BookListView, self).get_context_data(*args, **kwargs)
			context['books'] = Book.objects.all()
			return context

As discussed in last post on TemplateView, we didn't have to provide a get() implementation and didn't have to bother with render() while using TemplateView. All that was taken care of by TemplateView.

We only had to provide a get_context_data() implementation to add context to the template.

#### By subclassing ListView

	from django.views.generic.list import ListView

	class BookListView(ListView):
		template_name = 'book-list.html'
		queryset = Book.objects.all()
		context_object_name = 'books'

ListView removes more boilerplate from TemplateView. With ListView we didn't have to bother with get_context_data() implementation. ListView takes care of creating context variable 'books' and passing this context variable to template.

We can also add filtering in ListView.queryset.

	class BookListView(ListView):
		template_name = 'book-list.html'
		queryset = Book.objects.filter(name='A Feast for Crows')
		context_object_name = 'books'

Had we wanted pagination, we would have had to add several lines of code in TemplateView or vanilla View implementation. ListView provides pagination for free, we don't have to add pagination code.

Pagination can be added to ListView subclasses by setting a variable `paginate_by`

	class BookListView(ListView):
		template_name = 'book-list.html'
		queryset = Book.objects.all()
		context_object_name = 'books'
		paginate_by = 10

After this **/books-list/?page=1** will return first 10 books. **/books-list/?page=2** will return next 10 books and so on.

#### Further configuring ListView

If your list page's queryset doesn't need any filtering, and works with `.all()` on your model, then you can provide a `model` attribute on the BookListView instead of providing `queryset`.

	class BookListView(ListView):
		template_name = 'book-list.html'
		model = Book
		context_object_name = 'books'
		paginate_by = 10

You can add ordering to your queryset by adding `ordering` attribute on View. Suppose you want the books to be ordered in the page by their created date descending. You can do:

	class BookListView(ListView):
		template_name = 'book-list.html'
		model = Book
		context_object_name = 'books'
		paginate_by = 10
		ordering = [-created']

Since ordering is a list, so you can order by multiple attributes.

In case you want to filter the queryset differently for different web requests, then you can skip adding `model` or `queryset` on the list view and instead provide a `get_queryset()` implementation.

	class BookListView(ListView):
		template_name = 'book-list.html'
		context_object_name = 'books'
		paginate_by = 10
		ordering = [-created']

	    def get_queryset(self):
	        return Book.objects.filter(created_by=self.request.user)

You can avoid `template_name` attribute too. The default behaviour of ListView is to use a template with name `<app-label>/<model-name>_list.html`. You can change your BookListView to look like:

	class BookListView(ListView):
		model = Book
		context_object_name = 'books'
		paginate_by = 10

But then your template code should be in `books/book_list.html`. This assumes that your Book model is in app `books`. In case Book model is in, say `entitites` app, then template code should be in `entities/book_list.html`.

You can avoid `context_object_name` too. The default behaviour of ListView is to populate the template with context name `object_list`. You can change your BookListView to look like:

	class BookListView(ListView):
		model = Book
		paginate_by = 10

In such case your template code should change to:

	{% for book in object_list %}
	  {{book.name}}
	  <br/>
	{% endfor %}

Essentially a ListView helps you avoid boilerplate code like:

* providing a GET() implementation.
* Creating queryset with ordering.
* providing an encapsulated pagination code. Had we written pagination code in vanilla view, it would have easily added more 10 lines of code.
* providing the template with a sane context.
* creating and returning a HttpResponse() or a subclass of HttpResponse() object.

The **must** requirement for a ListView is, it must be provided with a `model` or `queryset` or a `get_queryset()` implementation. Every other piece has a sane default.
