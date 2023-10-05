from django.shortcuts import render, redirect
from .models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseServerError
import json


# Create your views here.
@login_required
def post_comment_create_and_list_view(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    

    # Initialization
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False

    if "submit_p_form" in request.POST:
        p_form = PostModelForm(request.POST or None, request.FILES or None)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True

    if "submit_c_form" in request.POST:
        print("c_form received")
        c_form = CommentModelForm(request.POST or None)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id = request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

    context = {
        'qs' : qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added
    }
    return render(request, 'posts/main.html', context )

@login_required
def like_unlike_post(request):
    user = request.user

    if request.method == 'POST':
        json_data = json.loads(request.body)
        # print(json_data)
        try:
            post_id=json_data['post_id']
        except KeyError:
            return HttpResponseServerError("Malformed Data")

        # post_id = request.POST.get('post_id')
        # print(f"post_id = {post_id}")
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
            new_like = "Unlike"
        else:
            post_obj.liked.add(profile)
            new_like = "Like"

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        print (f"like - {like.value}")
        print (f"created - {created}")

        like.value = new_like

        post_obj.save()
        like.save()

        data = {
            'likeTotal': post_obj.num_likes(),
            'likeValue': like.value,
        }

        print(data)
        return JsonResponse(data)
    
    return redirect('posts:main_post_view')

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main_post_view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request,'You need to be the author of the post in order to delete it')
        return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main_post_view')

    def form_valid(self, form):
        profile = Profile.objects.get(user = self.request.user)

        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You need to be author of the post in order to edit')
            return super().form_invalid(form)



       
        
