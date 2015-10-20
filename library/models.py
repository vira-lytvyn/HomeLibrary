from django.db import models
from django.contrib.auth.models import User

LITERATURE_GENRES = (
    ('1', 'Novel'),
    ('2', 'Poem'),
    ('3', 'Drama'),
    ('4', 'Short story'),
    ('5', 'Novella'),
    ('6', 'Myths'),
    ('7', 'Drama'),
    ('8', 'Romance'),
    ('9', 'Satire'),
    ('10', 'Tragedy'),
    ('11', 'Comedy'),
    ('12', 'Tragicomedy'),
    ('13', 'Science fiction'),
    ('14', 'Thriller')
)

GENDER_CHOICE = (
    ('m', 'Male'),
    ('m', 'Female'),
)

MARK_CHOICE = (
    ('g', 'Like it!'),
    ('n', 'Good for one time.'),
    ('b', 'Do not like it.'),
)

NOTES_TYPE_CHOICE = (
    ('h', 'History of appearance'),
    ('p', 'Reading progress'),
    ('f', 'Fanny stories'),
    ('c', 'Custom notes')
)

#
# class Series(models.Model):
#     name = models.CharField(max_length=128)


class Genre(models.Model):
    name = models.CharField(max_length=1, choices=LITERATURE_GENRES, default='0', unique=True)

    def __unicode__(self):
        genres = dict(LITERATURE_GENRES)
        return genres[self.name]


class PublishingHouse(models.Model):
    name = models.CharField(max_length=128)
    founded = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="staticImages/publishingHouseLogo/", blank=True, null=True)

    def __unicode__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    pseudo_name = models.CharField(max_length=80, default='Unknown', blank=True, null=True)
    awards = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    publishers = models.ForeignKey(PublishingHouse, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fb_account = models.URLField(blank=True, null=True)
    photo = models.ImageField(upload_to="staticImages/authorPhoto/", blank=True, null=True)
    # books = models.ManyToManyField(Book, blank=True, null=True)
    rate = models.PositiveSmallIntegerField(default=0)
    genres = models.ManyToManyField(Genre, blank=True)

    def __unicode__(self):
        return self.pseudo_name


class Book(models.Model):
    title = models.CharField(max_length=128)
    authors = models.ForeignKey(Author, blank=True, null=True)
    publisher = models.ForeignKey(PublishingHouse, blank=True, null=True)
    year = models.DateField(blank=True, null=True)
    added = models.DateField(blank=True, null=True)
    isbn_number = models.CharField(max_length=13, blank=True, null=True)
    pages = models.PositiveIntegerField(blank=True, null=True)
    annotation = models.CharField(max_length=255, blank=True, null=True)
    currently_read = models.CharField(max_length=10, blank=True, null=True)
    present_status = models.BooleanField(default=False)
    favourite_for = models.ForeignKey(User, blank=True, null=True)
    cover = models.ImageField(upload_to="staticImages/authorPhoto/", blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)

    def __unicode__(self):
        return self.title

    def get_owners(self):
        return UserProfile.objects.filter(owner_of_books__in=[self])

    def get_authors(self):
        return self.authors.all()

    def get_notes(self):
        return CustomNote.objects.filter(book__in=[self])

    def get_all_review(self):
        return Review.objects.filter(book__in=[self])


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    read_books = models.ManyToManyField(Book, blank=True, related_name='read books', null=True)
    owner_of_books = models.ManyToManyField(Book, blank=True, related_name='owner of books', null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    favourite_books = models.ForeignKey(Book, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    def has_read_the_book(self, book_id):
        if book_id in self.read_books.all():
            return True
        return False

    def is_one_of_favourite(self, book_id):
        if book_id in self.favourite_books.all():
            return True
        return False

    def is_owner_of_book(self, book_id):
        if book_id in self.owner_of_books.all():
            return True
        return False

    def get_favourites(self):
        return Book.objects.filter()

    def get_all_quotes(self):
        return Quote.objects.filter(author__in=[self])

    def get_all_notes(self):
        return CustomNote.objects.filter(author__in=[self])

    def get_all_review(self):
        return Review.objects.filter(author__in=[self])


class Quote(models.Model):
    book = models.ForeignKey(Book)
    author = models.ForeignKey(User)
    text = models.CharField(max_length=250)
    page = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.text


class Review(models.Model):
    book = models.ForeignKey(Book)
    author = models.ForeignKey(User)
    text = models.CharField(max_length=250, blank=True, null=True)
    mark = models.CharField(max_length=1, choices=MARK_CHOICE)

    def __unicode__(self):
        return self.text


class CustomNote(models.Model):
    book = models.ForeignKey(Book)
    author = models.ForeignKey(User)
    text = models.CharField(max_length=250)
    type = models.CharField(max_length=1, choices=NOTES_TYPE_CHOICE, blank=True, null=True)

    def __unicode__(self):
        return self.text
