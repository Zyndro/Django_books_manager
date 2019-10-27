import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import BooksForm
from .models import Books


def is_valid_queryparam(param):
    return param != '' and param is not None


def index(request):
    queryset = Books.objects.all()
    query = request.GET.get("title")
    querya = request.GET.get("author")
    queryl = request.GET.get("language")
    startyear = request.GET.get("startyear")
    endyear = request.GET.get("endyear")
    if is_valid_queryparam(query):
        queryset = Books.objects.filter(title__icontains=query)
    if is_valid_queryparam(querya):
        queryset = Books.objects.filter(authors__icontains=querya)
    if is_valid_queryparam(queryl):
        queryset = Books.objects.filter(language__icontains=queryl)
    if is_valid_queryparam(startyear):
        queryset = Books.objects.filter(publishedDate__gte=startyear)
    if is_valid_queryparam(endyear):
        queryset = Books.objects.filter(publishedDate__lte=endyear)
    context = {
        "object_list": queryset}
    return render(request, 'book/list.html', context)


def add_book(request):
    if request.method == "POST":
        form=BooksForm(request.POST)
        if form.is_valid():
            book_item=form.save(commit=False)
            book_item.save()
            return HttpResponseRedirect('/')
    else:
        form=BooksForm()
    return render(request, 'book/book_form.html', {'form': form})


def google_import(request):
    list = []
    counter = 0
    query = request.GET.get("title")
    if is_valid_queryparam(query):
        url = 'https://www.googleapis.com/books/v1/volumes?q={}&printType=books'
        url = url.format(query)
        r = requests.get(url)
        results=r.json()['items']
        for result in results:
            try:
                book = {
                    'title': result['volumeInfo']['title'],
                    'authors': result['volumeInfo']['authors'],
                    'publishedDate': result['volumeInfo']['publishedDate'],
                    'industryIdentifiers': result['volumeInfo']['industryIdentifiers'],
                    'pageCount': result['volumeInfo']['pageCount'],
                    'imageLinks': result['volumeInfo']['imageLinks'],
                    'language': result['volumeInfo']['language'],
                }


                list.append(book)
                counter += 1
            except KeyError:
                pass

    if request.method == "POST":
        number = request.POST.get("number")
        try:
            form = BooksForm(list[int(number)-1])
            if form.is_valid():
                book_item=form.save(commit=False)
                book_item.save()
                counter = "imported book nr:"+number
        except IndexError:
            counter="wrong index number"





    return render(request, 'book/book_import.html', {'r':list, 'counter':counter})