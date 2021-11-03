from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView
from .models import Post,Vote,Comment
from .forms import CommentForm,PostForm
 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
 
from datetime import datetime,timedelta
from django.utils import timezone
 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

 
 
def post_list_view(request):
    posts = Post.objects.all()
    for post in posts:
        post.count_votes()
        post.count_comments()
         
    context = {
        'posts': posts,
    }
    return render(request,'nhapp/postlist.html',context)
 
 
def new_post_list_view(request):
    posts = Post.objects.all().order_by('-created_date')
    for post in posts:
        post.count_votes()
        post.count_comments()    
    context = {
        'posts': posts,
    }
    return render(request,'nhapp/postlist.html', context)
 
 
def past_post_list_view(request):
    time = str((datetime.now(tz=timezone.utc) - timedelta(hours=24)))
    posts = Post.objects.filter(created_date__lte = time)
    for post in posts:
        post.count_votes()
        post.count_comments()
 
    context={
        'posts': posts,
    }
    return render(request,'nhapp/postlist.html',context)
 
 
def up_vote_view(request,id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        amount_of_upvotes= Vote.objects.filter(post = post)
        v = amount_of_upvotes.filter(voter = request.user)
        if len(v) == 0:
            upvote = Vote(voter=request.user,post=post)
            upvote.save()
            return redirect('/')
    return redirect('/signin')
 
 
def down_vote_view(request,id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        amount_of_upvotes = Vote.objects.filter(post = post)
        v = amount_of_upvotes.filter(voter = request.user)
        if len(v) != 0:
            v.delete()
            return redirect('/')
    return redirect('/signin')    
 
 
def user_info_view(request,username):
    user = User.objects.get(username=username)
    context = {'user':user,}
    return render(request,'nhapp/user_info.html',context)
 
 
def user_submissions(request,username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author_name = user)
    print(len(posts))
    for post in posts:
        post.count_votes()
        post.count_comments()    
    return render(request,'nhapp/user_post.html',{'posts': posts})
   
 
def edit_list_view(request,id):
    post = get_object_or_404(Post,id=id)
    if request.method =='POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')
     
    form = PostForm(instance =post)
    return render(request,'nhapp/submit.html',{'form':form})
 
 
def comment_list_view(request,id):
    form = CommentForm()
    post = Post.objects.get(id =id)
    post.count_votes()
    post.count_comments()
 
    comments = []    
    def func(i,parent):
        children = Comment.objects.filter(post =post).filter(identifier =i).filter(parent=parent)
        for child in children:
            gchildren = Comment.objects.filter(post =post).filter(identifier = i+1).filter(parent=child)
            if len(gchildren)==0:
                comments.append(child)
            else:
                func(i+1,child)
                comments.append(child)
    func(0,None)
 
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                comment = Comment(author_name = request.user,post = post,content = content,identifier =0)
                comment.save()
                return redirect(f'/post/{id}')
        return redirect('/signin')
 
    context ={
        'form': form,
        'post': post,
        'comments': list(reversed(comments)),
    }
    return render(request,'nhapp/commentpost.html', context)
 
 
def comment_reply_view(request,id1,id2):
    form = CommentForm()
    comment = Comment.objects.get(id = id2)
    post = Post.objects.get(id=id1)
 
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
             
            if form.is_valid():
                reply_comment_content = form.cleaned_data['content']
                identifier = int(comment.identifier + 1)
 
                reply_comment = Comment(author_name = request.user, post = post, content = reply_comment_content, parent=comment, identifier= identifier)
                reply_comment.save()
 
                return redirect(f'/post/{id1}')
        return redirect('/signin')
     
    context ={
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request,'nhapp/reply_post.html', context)
 
 
def submit_post_view(request):
    if request.user.is_authenticated:
        form = PostForm()
 
        if request.method == "POST":
            form = PostForm(request.POST)
 
            if form.is_valid():
                title = form.cleaned_data['title']
                link = form.cleaned_data['link']
                description = form.cleaned_data['description']
                author_name = request.user
                created_date = datetime.now()
 
                post = Post(title=title, link = link , description=description, author_name = author_name, created_date = created_date)
                post.save()
                return redirect('/')
        return render(request,'nhapp/submit.html',{'form':form})
    return redirect('/signin')
 
 
def signup(request):
 
    if request.user.is_authenticated:
        return redirect('/')
     
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
 
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username,password = password)
            login(request, user)
            return redirect('/')
         
        else:
            return render(request,'nhapp/auth_signup.html',{'form':form})
     
    else:
        form = UserCreationForm()
        return render(request,'nhapp/auth_signup.html',{'form':form})
 
 
def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            form = AuthenticationForm()
            return render(request,'nhapp/auth_signin.html',{'form':form})
     
    else:
        form = AuthenticationForm()
        return render(request, 'nhapp/auth_signin.html', {'form':form})
 
 
def signout(request):
    logout(request)
    return redirect('/')