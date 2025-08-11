# Building Custom Views and Generic Views in Django REST Framework
# Book API - View Configurations
This API manages Book resources with endpoints for listing, retrieving, creating, updating, and deleting books. Views are implemented using Django REST Framework's generic views to streamline CRUD operations.

## Endpoints and Permissions

| Method | Endpoint                | View Class        | Description                              | Permissions        |
|--------|-------------------------|-------------------|------------------------------------------|--------------------|
| GET    | /api/books/             | BookListView      | List all books                           | Public (AllowAny)  |
| GET    | /api/books/<pk>/        | BookDetailView    | Retrieve a book by ID                    | Public (AllowAny)  |
| POST   | /api/books/create/      | BookCreateView    | Create a new book                        | Authenticated only |
| PUT    | /api/books/<pk>/update/ | BookUpdateView    | Update an existing book                  | Authenticated only |
| PATCH  | /api/books/<pk>/update/ | BookUpdateView    | Partially update an existing book        | Authenticated only |
| DELETE | /api/books/<pk>/delete/ | BookDeleteView    | Delete an existing book                  | Authenticated only |

## Custom Hooks
- **perform_create()**: Validates that `publication_year` is >= 1450 before saving.
- **perform_update()**: Applies the same validation during book updates.

## Notes
- Validation errors raise an exception before saving data to the database.
- Permissions are enforced using DRF's built-in `IsAuthenticated` and `AllowAny` classes.




# Implementing Filtering, Searching, and Ordering in Django REST Framework
## Filtering, Searching, and Ordering

The `/api/books/` endpoint supports advanced query capabilities:

### Filtering
Exact match filtering by:
- `title`
- `author` (author ID)
- `publication_year`
Example:
GET /api/books/?title=1984&publication_year=1949

### Searching
Partial match search (case-insensitive) by:
- `title`
- `author`'s name

Example:
GET /api/books/?search=potter
GET /api/books/?search=rowling

### Ordering
Sort results by:
- `title`
- `publication_year`

Example:
GET /api/books/?ordering=publication_year

Default ordering: `title` ascending.

