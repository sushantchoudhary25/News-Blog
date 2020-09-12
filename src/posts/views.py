from django.shortcuts import render
from .models import Post
from marketing.models import Signup


# Create your views here.
def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == 'POST':
        email = request.POST.get('email')

        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list' : featured,
        'latest' : latest
    }

    return render(request, 'posts/index.html', context=context)


def blog(request):
    return render(request, 'posts/blog.html')


def post(request):
    return render(request, 'posts/post.html')