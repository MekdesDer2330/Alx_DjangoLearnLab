from relationship_app.models import Author, Book, Library, Librarian

author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)
library = Library.objects.get(name=library_name)
librarian = library.librarian


# Query all books by a specific author
def books_by_author(author_name):
    books = Book.objects.filter(author__name=author_name)
    return books

# List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

# Retrieve the librarian for a library
def librarian_of_library(library_name):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)
