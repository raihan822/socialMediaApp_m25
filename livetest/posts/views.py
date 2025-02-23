from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post

from django.db.models import Q
from .forms import PostForm, PostFilterForm
from django.contrib import messages

def home(request):
    posts = Post.objects.all().select_related('user')
    form = PostFilterForm(request.GET)
    
    # Apply filters
    if form.is_valid():
        search = form.cleaned_data.get('search')
        sort = form.cleaned_data.get('sort')
        media_type = form.cleaned_data.get('media_type')
        author = form.cleaned_data.get('author')

        # Search filter
        if search:
            posts = posts.filter(Q(content__icontains=search))

        # Author filter
        if author:
            posts = posts.filter(user__username__icontains=author)

        # Media type filter
        if media_type and media_type != 'all':
            posts = posts.filter(media_type=media_type)

        # Sorting
        if sort == 'oldest':
            posts = posts.order_by('created_at')
        else:
            posts = posts.order_by('-created_at')

    return render(request, 'posts/home.html', {
        'posts': posts,
        'form': form
    })


@login_required
def profile(request):
    posts = Post.objects.filter(user=request.user).select_related('user')
    form = PostFilterForm(request.GET)
    
    # Apply filters (excluding author filter)
    if form.is_valid():
        search = form.cleaned_data.get('search')
        sort = form.cleaned_data.get('sort')
        media_type = form.cleaned_data.get('media_type')

        if search:
            posts = posts.filter(Q(content__icontains=search))

        if media_type and media_type != 'all':
            posts = posts.filter(media_type=media_type)

        if sort == 'oldest':
            posts = posts.order_by('created_at')
        else:
            posts = posts.order_by('-created_at')

    return render(request, 'posts/profile.html', {
        'posts': posts,
        'form': form
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Post created!')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('profile')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted!')
    return redirect('profile')