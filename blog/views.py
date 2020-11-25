from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

#api
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

#local
from .serializers import PostSerializer
from .forms import CommentForm, SearchForm
from .models import Post
from taggit.models import Tag


def about(request):
    return render(request, 'about.html')


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 6)  # 6 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})


# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 6
#     template_name = 'blog/list.html'


def post_detail(request, uuid):
    post = get_object_or_404(Post, uuid=uuid)

    # List of active comments for this post
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(uuid=post.uuid)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]

    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


def post_search(request):
    search_form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            search_vector = SearchVector('title', 'description')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')

            # paginator = Paginator(request, results, 6)
    context = {
        'search_form': search_form,
        'query': query,
        'results': results
    }

    return render(request,
                  'blog/search.html', context)


@api_view(['GET'])
def post_api_list(request):
    if request.method == 'GET':
        emp = Post.objects.all()
        serializer = PostSerializer(emp, many=True)
        return Response(serializer.data)

    # elif request.method == 'POST':
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
@api_view(['GET'])
def post_api_details(request, uuid):
    try:
        post = Post.objects.get(uuid=uuid)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    # elif request.method == 'PUT':
    #     serializer = PostSerializer(emp, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # elif request.method == 'DELETE':
    #     emp.delete()
    #     return Response(status= status.HTTP_204_NO_CONTENT)