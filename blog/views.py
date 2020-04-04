from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


def home(request):
    context = {         #JSON style
        'posts': Post.objects.all()
    }
    return render(request, "blog/home.html", context)

class PostListView(ListView):
    '''
        This class is responsible for viewing a list of Posts in the blog as a ListView
    '''
    model = Post
    template_name = 'blog/home.html' # The Template that would be rendered. <app>/<model>_<viewtype>.html
    context_object_name = 'posts' #The name of the object that it would be looping for 
    ordering = ['-date_posted']  #Sort. - sign means newest to oldest
    paginate_by = 5     # How to paginate a page. This one is how many items in a list


class UserPostListView(ListView):
    '''
        This class is responsible for viewing a list of Posts in the blog created by the User as a ListView

        This is similar to PostListView. However, the diffference is that we filter only the posts created by the "clicked" User
        How? We can base it on the URL pattern  when clicked. 
    '''
    model = Post
    template_name = 'blog/user_posts.html' # The Template that would be rendered. <app>/<model>_<viewtype>.html
    context_object_name = 'posts' #The name of the object that it would be looping for 
    # This is overriden by due to overriding get_query_set.  ordering = ['-date_posted']  #Sort. - sign means newest to oldest
    paginate_by = 5     # How to paginate a page. This one is how many items in a list

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) #kwargs is to get params from URL
        return Post.objects.filter(author=user).order_by('-date_posted')


# If we want to click each post to read the content of the blog, that's called DetailView

class PostDetailView(DetailView):
    model = Post

# In the succeeding class, we investigate how to create,read,update,delete (CRUD)
# How to create a new Post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    #success_url = 'blog/home.html'  #In case you want to go home afterwards. You can simply set this attrib.
    # Currently, each newly created post redirects to its detailView as seen in Model get_absolute_url
    def form_valid(self, form):
        ''' We are overriding the form valid method so that we can include 
        the author_id as currently logged in id.
        '''
        form.instance.author = self.request.user
        return super().form_valid(form) # Runs the form valid method before super class. It always runs anyway
        

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        ''' We are overriding the form valid method so that we can include 
        the author_id as currently logged in id.
        '''
        form.instance.author = self.request.user
        return super().form_valid(form) # Runs the form valid method before super class. It always runs anyway
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




def about(request):
    return render(request, "blog/about.html", {"title": "About"})


