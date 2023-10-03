from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from .models import News, Category
from .forms import ContactForm

def news_list(request):
    news_list = News.objects.all()

    context = {
        'news_list':news_list
    }
    return render(request, 'news/news_list.html', context = context)

def news_detail(request, news):
    news = get_object_or_404(News, slug = news, status = News.Status.Published)

    context = {
        'news':news
    }
    return render(request, 'news/news_detail.html', context)

# def HomePageView(request):
#     news_list = News.published.all().order_by('-publish_time')[:5]
#     categories = Category.objects.all()
#     local_one = News.published.all().filter(category__name = 'Mahalliy')[:1]
#     local_news = News.published.all().filter(category__name = 'Mahalliy')[1:6]
#
#     context = {
#         'news_list':news_list,
#         'categories':categories,
#         'local_one':local_one,
#         'local_news':local_news
#     }
#
#     return render(request, 'news/home.html', context)


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