from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from blog.forms import CreatePostForm
from blog.models import Post


def index(request):
    posts = Post.objects.all().order_by('-created_at')
    # template = loader.get_template('blog/index.html')

    context = {
        'all_posts': posts
    }

    # return HttpResponse(template.render(context, request))
    return render(request, 'blog/index.html', context)


def detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/detail.html', {
        "post": post
    })
    # return HttpResponse(f"<h1> id: {p.id}. {p.title} </h1>"
    #                     f"<p> {p.content} test </p>")


def new_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)
            post.author_id = 1
            post.save()

            return redirect("index")
        else:
            return HttpResponse('Error creating!')

    # GET
    context = {
        'form': CreatePostForm()
    }

    return render(request,
                  'blog/create_post.html',
                  context=context)

# def posts(request):
#     post_id = request.GET.get('id', 1)
#     p = Post.objects.get(id=post_id)
#     return HttpResponse(f"<h1> id: {p.id}. {p.title} </h1>"
#                         f"<p> {p.content} test </p>")

# def index(request):
#     posts = Post.objects.all().order_by('-created_at')
#     response = (f"<ul>"
#                 f"{ ''.join([f'<li>{post.title}</li>' for post in posts]) }"
#                 f"</ul>")
#     return HttpResponse(response)