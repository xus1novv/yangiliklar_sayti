from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView,UpdateView, CreateView, DeleteView, DetailView
from .models import News
from .forms import ContactForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class OnlyLoggedSuperUser(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

def news_list(request):
    news_list = News.objects.all()

    context = {
        'news_list':news_list
    }
    return render(request, 'news/news_list.html', context = context)

@login_required
def news_detail(request, news):
    news = get_object_or_404(News, slug = news, status = News.Status.Published)
    comments = news.comments.filter(active=True)
    comments_count = comments.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            #yangi comment obyektini yaratamiz lekin DB ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            # commit=False bu yangilikni DB ga saqlamay ushlab turadi

            new_comment.news = news
            #izoh egasini request yuborayotgan userga bog'ladik
            new_comment.user = request.user
            #malumotlar bazasiga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'news':news,
        'comments':comments,
        'comments_count':comments_count,
        'new_comment':new_comment,
        'comment_form':comment_form
    }
    return render(request, 'news/news_detail.html', context)

class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.published.all()[:5]
        context['mahalliy_news'] = News.published.all().filter(category__name = 'Mahalliy')[:5]
        context['sport_news'] = News.published.all().filter(category__name = 'Sport')[:5]
        context['xorij_news'] = News.published.all().filter(category__name = 'Xorij')[:5]
        context['texnologiya_news'] = News.published.all().filter(category__name = 'Texnologiya')[:5]


        return context


# def ContactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse('OK')
#
#
#     context = {
#         'form':form
#     }
#     return render(request, 'news/contact.html', context)

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form':form
        }

        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()

            return HttpResponse('Biz bilan bog\'langaningiz uchun tashakkur')
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)


class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mah_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'Mahalliy')
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'spo_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'Sport')
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texno.html'
    context_object_name = 'tex_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'Texnologiya')
        return news


class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xor_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'Xorij')
        return news


class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status', )
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title','slug','body','image','category','status')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_page_view(request):

    admin_info = User.objects.filter(is_superuser=True)
    context = {
        'admin_info':admin_info
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'qidiruv_yangiliklari'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.published.all().filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
