from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Post
from .forms import CommentForm
from marketing.models import Signup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    context = {
        'queryset' : queryset
    }
    return render(request, 'search_results.html', context=context)


def get_category_count():
    queryset = Post.\
        objects.\
        values('categories__title').\
        annotate(Count('categories__title'))
    return queryset


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == 'POST':
        email = request.POST.get('email')

        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest
    }

    return render(request, 'posts/index.html', context=context)


def blog(request):
    category_count = get_category_count()
    post_list = Post.objects.all()
    latest = Post.objects.order_by('-timestamp')[0:3]
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'latest' : latest,
        'category_count' : category_count
    }
    return render(request, 'posts/blog.html', context)


def post(request, id):
    category_count = get_category_count()
    latest = Post.objects.order_by('-timestamp')[0:3]
    post = get_object_or_404(Post, id=id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post', kwargs={
                'id' : post.id
            }))
        
    context = {
        'form' : form,
        'post' : post,
        'latest': latest,
        'category_count': category_count
    }
    return render(request, 'posts/post.html', context)
