import graphene
from graphene_django.types import DjangoObjectType
from .models import Book

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "author")

class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book_by_title = graphene.Field(BookType, title=graphene.String())

    def resolve_all_books(root, info):
        return Book.objects.all()

    def resolve_book_by_title(root, info, title):
        try:
            return Book.objects.get(title=title)
        except Book.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)
