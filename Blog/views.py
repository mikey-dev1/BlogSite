
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.views import LoginView,LogoutView

from .models import *
from django.db.models import Q
from taggit.models import Tag
from django.http import HttpResponseRedirect
# Create your views here.


def Signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'Blog/registration.html', {'form': form})


def home(request):
    posts = Post.objects.filter(status = 'published')
    recent_posts = posts[0:3]
    category = Categories.objects.all()
    
    return render(request,'Blog/home.html',{'posts':posts,'recent_posts':recent_posts,'category':category})

class Login(LoginView):
  form_class = MyLoginForm
 







def Search_Result(request):
    #search
  
    if request.method == 'POST':
        print(request.POST['query'])
        query = request.POST['query']
        posts = Post.published.filter(Q(title__icontains = query) | Q(tags__name__icontains = query)).distinct()
    else:
        query = ''
        posts = ''
    #recent post
    recent_posts  = Post.objects.filter(status = 'published')[0:3]
    return render(request,'Blog/search.html',{'posts':posts,'recent_posts':recent_posts,'query':query})


def Post_Detail(request,pk):
    #get post object by id
   
    post = Post.objects.get(id = pk)
    comments = post.comments.filter(active = True)
    recent_posts  = Post.objects.filter(status = 'published')[0:3]
    category = Categories.objects.all()
  
    comment_form = CommentForm(data = request.POST)
    if request.method == 'POST' and comment_form.is_valid():
        
        body = comment_form.cleaned_data['body']

        try:
            parent = comment_form.cleaned_data['parent']
        except:
            parent = None
    
        new_comment = BlogComment(body = body,User = request.user,post = post,parent = parent)
        new_comment.save()
        comment_form = CommentForm()

    return render(request,'Blog/post_detail.html',{'post':post,'recent_posts':recent_posts,
    'category':category,'comments':comments,
    'comment_form':comment_form })





def Category(request,category):
    cate = category
    print(Post.objects.filter(category__title = category))
    posts = Post.objects.filter(category__title = category)
    recent_posts  = Post.objects.filter(status = 'published')[0:3]
    return render(request,'Blog/category.html',{'posts':posts,'cate':cate,'recent_posts':recent_posts,})