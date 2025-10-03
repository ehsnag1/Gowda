from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, MovieRequest, Petition, PetitionVote
from django.contrib.auth.decorators import login_required
from .forms import MovieRequestForm, PetitionForm
from django.http import JsonResponse

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def movie_requests(request):
    if request.method == 'POST':
        form = MovieRequestForm(request.POST)
        if form.is_valid():
            movie_request = form.save(commit=False)
            movie_request.user = request.user
            movie_request.save()
            return redirect('movies.movie_requests')
    else:
        form = MovieRequestForm()
    
    # Get all movie requests for the current user
    user_requests = MovieRequest.objects.filter(user=request.user).order_by('-date')
    
    template_data = {}
    template_data['title'] = 'Movie Requests'
    template_data['form'] = form
    template_data['requests'] = user_requests
    
    return render(request, 'movies/movie_requests.html', {'template_data': template_data})

@login_required
def delete_movie_request(request, request_id):
    movie_request = get_object_or_404(MovieRequest, id=request_id, user=request.user)
    movie_request.delete()
    return redirect('movies.movie_requests')

def petitions(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.creator = request.user
            petition.save()
            return redirect('movies.petitions')
    else:
        form = PetitionForm()
    
    # Get all petitions ordered by date (newest first)
    petitions_list = Petition.objects.all().order_by('-date')
    
    # Add user vote information to each petition if user is authenticated
    if request.user.is_authenticated:
        for petition in petitions_list:
            petition.user_has_voted = petition.has_user_voted(request.user)
            petition.user_vote = petition.get_user_vote(request.user)
    
    template_data = {}
    template_data['title'] = 'Movie Petitions'
    template_data['form'] = form
    template_data['petitions'] = petitions_list
    
    return render(request, 'movies/petitions.html', {'template_data': template_data})

@login_required
def vote_petition(request, petition_id):
    if request.method == 'POST':
        petition = get_object_or_404(Petition, id=petition_id)
        vote_type = request.POST.get('vote_type')
        
        if vote_type in ['yes', 'no']:
            # Check if user already voted
            existing_vote = PetitionVote.objects.filter(petition=petition, user=request.user).first()
            
            if existing_vote:
                # Update existing vote
                existing_vote.vote_type = vote_type
                existing_vote.save()
            else:
                # Create new vote
                PetitionVote.objects.create(
                    petition=petition,
                    user=request.user,
                    vote_type=vote_type
                )
        
        return redirect('movies.petitions')
    
    return redirect('movies.petitions')

 