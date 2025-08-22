from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .models import Book
from .forms import ExampleForm

def index(request):
    return HttpResponse("Welcome to the Book Shelf!")

def example_form_view(request):
    form = ExampleForm(request.POST or None)
    if form.is_valid():
        # Do something with the form data if needed
        return HttpResponse("Form submitted successfully!")
    return render(request, 'bookshelf/form_example.html', {'form': form})


def search_books(request):
    form = BookSearchForm(request.GET or None)
    results = []
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'form': form, 'results': results})

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect('index')
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book deleted successfully!")

