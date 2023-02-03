from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Movie, Reviews
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required


def index(request):
    searchTerm=request.GET.get('searchMovie')
    if searchTerm:
        movies=Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies=Movie.objects.all()
    return render(request, 'index.html', {'name': searchTerm, 'movies': movies})

def signup(request):
    email=request.GET.get('email')
    return render(request, 'signup.html', {'email': email})


def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Reviews.objects.filter(movie=movie)
    return render(request, 'details.html', {'movie': movie, 'reviews': reviews})

@login_required
def createreview(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'GET':
        return render(request, 'createreview.html', {'form': ReviewForm(), 'movie': movie})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.movie = movie
            newReview.save()
            return redirect('detail', newReview.movie.id)
        except ValueError:
            return render(request, 'createreview.html', {'form':ReviewForm(), 'error': 'Bad data passed in'})
            

@login_required
def updatereview(request, review_id):
    review=get_object_or_404(Reviews, pk=review_id, user=request.user)
    if request.method == 'GET':
        form = ReviewForm(instance = review)
        return render(request, 'updatereview.html', {'review':review, 'form':form})
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', review.movie.id)
        except ValueError:
            return render(request, 'updatereview.html', {'review':review, 'form':form, 'error':'Bad data in form'})

@login_required
def deletereview(request, review_id):
    review = get_object_or_404(Reviews, pk=review_id, user=request.user)
    review.delete()
    return redirect('detail', review.movie.id)