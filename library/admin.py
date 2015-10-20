from django.contrib import admin
from library.models import Book, Author, PublishingHouse, UserProfile


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'publisher', 'isbn_number')


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(PublishingHouse)
admin.site.register(UserProfile)
