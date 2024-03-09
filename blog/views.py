from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.template import loader

from blog.forms import CreatePostForm, CreateCommentForm
from blog.models import Post, Comment


def index(request):
    posts = Post.objects.all().order_by('-created_at')
    # template = loader.get_template('blog/index.html')

    context = {
        'all_posts': posts
    }

    # return HttpResponse(template.render(context, request))
    return render(request, 'blog/index.html', context)

# COMMENTS + COMMENTING FORM ARE IMPLEMENTED HERE
class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    form_class = CreateCommentForm

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('post_id')
        return self.model.objects.get(pk=post_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.request.path

# def detail(request, post_id):
#
#     # if a comment is posted
#     if request.method == 'POST':
#         form = CreateCommentForm(request.POST)
#
#         if form.is_valid():
#
#             comment = form.save(commit=False)
#             comment.post_id = post_id
#             comment.save()
#
#             return HttpResponseRedirect(request.path_info)  # refresh this page
#         else:
#             return HttpResponse('Error creating!')
#
#     return render(request, 'blog/detail.html', {
#         "post": Post.objects.get(id=post_id),
#         "comments": Post.objects.get(id=post_id).comments.all(),
#         "form": CreateCommentForm()
#     })


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