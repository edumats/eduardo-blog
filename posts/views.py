from django.urls import reverse_lazy, reverse
from django.db.models import Count, Q
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.html import escape
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import CreatePostForm, CreateCategoryForm, UploadImage


def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset


def latest_posts():
    queryset = Post.objects.order_by('-created')[:3]
    return queryset


class IndexView(ListView):
    model = Post
    queryset = Post.objects.filter(featured=True)[:3]
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = latest_posts()
        return context


class PostListView(ListView):
    paginate_by = 4
    model = Post
    # Receiving UnorderedObjectListWarning before overriding the queryset
    queryset = Post.objects.order_by('-created')
    template_name = '../templates/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = latest_posts()
        context['category_count'] = get_category_count()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = '../templates/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = latest_posts()
        context['category_count'] = get_category_count()
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = '__all__'
    template_name = '../templates/post_update_form.html'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = '../templates/post_delete_form.html'
    success_url = reverse_lazy('index')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = '../templates/post_create_form.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class SearchView(ListView):
    paginate_by = 10
    model = Post
    template_name = '../templates/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = latest_posts()
        context['category_count'] = get_category_count()
        return context

    def get_queryset(self):
        query = self.request.GET.get('search')
        return Post.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(categories__title__icontains=query)
        ).distinct().order_by('-created')


class CategoryListView(ListView):
    paginate_by = 10
    model = Post
    template_name = '../templates/posts_list_by_category.html'

    def get_queryset(self):
        return Post.objects.filter(categories__title=self.kwargs['category']).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = latest_posts()
        context['category_count'] = get_category_count()
        context['category'] = self.kwargs['category']
        return context


def CreateCategoryView(request):
    if request.method == 'POST':
        print('posted')
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            print('form is valid')
            form.save()
            return HttpResponseRedirect(reverse('post-create'))


def handlePopAdd(request, addForm, field):
    if request.method == "POST":
        form = addForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                newObject = form.save()
            except form.ValidationError:
                newObject = None
            if newObject:
                return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddRelatedObjectPopup(window, "%s", "%s");</script>'
                    % escape(newObject._get_pk_val()), escape(newObject))
    else:
        form = addForm()
    pageContext = {'form': form, 'field': field}
    return render(request, "form/formpopup.html", pageContext)


@login_required
def newImage(request):
    return handlePopAdd(request, UploadImage, 'thumbnail')


@login_required
def newCategory(request):
    return handlePopAdd(request, CreateCategoryForm, 'categories')
