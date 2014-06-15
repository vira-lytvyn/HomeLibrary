from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from models import UserProfile, Book, Author, PublishingHouse

# Create your views here.


@csrf_exempt
def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    form = AuthenticationForm(None, request.POST or None)
    nextpage = request.GET.get('next', '/')

    if form.is_valid():
        login(request, form.get_user())
        return HttpResponseRedirect(nextpage)

    return render(request, 'login.html', {'form': form, 'next': nextpage})


@csrf_exempt
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@csrf_exempt
def index(request):
    latest_3_books = Book.objects.order_by('-added')[:3]
    return render(request, 'library/index.html', {'newest': latest_3_books})


@csrf_exempt
def view_user_profile(request, user_id):
    user = request.user
    requested_user = User.objects.get(id=user_id)
    user_profile = UserProfile.objects.get(user=requested_user)
    return render(request, 'library/user_page.html')


@csrf_exempt
def view_book(request, book_id):
    return render(request, 'library/book_page.html')


@csrf_exempt
def view_author(request, author_id):
    return render(request, 'library/author_page.html')


@csrf_exempt
def view_publisher(request, publisher_id):
    return render(request, 'library/publishing_house_page.html')


@csrf_exempt
def add_book(request):
    return render(request, 'library/add_book.html')


@csrf_exempt
def add_author(request):
    return render(request, 'library/add_author.html')


@csrf_exempt
def add_publish_house(request):
    return render(request, 'library/add_publisher.html')


@csrf_exempt
def view_all_book(request):
    # watched_list = []
    # will_watch_list = []
    # favourite_list = []
    # for movie in Movie.objects.all():
    #     if movie.status == 'w':
    #         watched_list.append(movie)
    #     elif movie.status == 'p':
    #         will_watch_list.append(movie)
    #     elif movie.status == 'f':
    #         favourite_list.append(movie)

    # return render(request, "manager/my_movies.html", {
    #     'watched': watched_list, 'will_watch': will_watch_list, 'favourite': favourite_list
    # })
    return render(request, 'library/books.html', {'books_list': Book.objects.all()})