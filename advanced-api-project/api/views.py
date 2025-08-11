from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer


# Book List View (GET) to retrieve all books
#filtering- by title, author and publication_year
#searching- by title or author's name
#ordering- by title or publication_year
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    #enable filtering, seraching and ordering
    filter_backends=[
	DjangoFilterBackend,
	filters.SearchFilter,
	filters.OrderingFilter
    ]

    # Filtering: matches exact values for fields
    filterset_fields = ['title', 'author', 'publication_year']

    # Searching: allows partial matches (case-insensitive)
    # The double underscore (__) allows searching across relationships
    search_fields = ['title', 'author__name']

    # Ordering: allows sorting results by these fields
    ordering_fields = ['title', 'publication_year']

    # Default ordering when no ?ordering param is provided
    ordering = ['title']


# Book Detail View (GET) to retrieve a single book by ID.
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 


# Book Create View (POST) to create a new book.
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 
	
    def perform_create(self, serializer):
        if serializer.validated_data['publication_year'] < 1450:
            raise ValueError("Publication year must be after the invention of the printing press.")
        serializer.save()


# Book Update View (PUT/PATCH) to update an existing book.
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.validated_data['publication_year'] < 1450:
            raise ValueError("Publication year must be after the invention of the printing press.")
        serializer.save()


# Book Delete View (DELETE) to delete an existing book.
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]





