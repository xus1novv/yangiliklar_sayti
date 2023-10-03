from  .models import News,Category

def common_info(request):
    latest_new = News.published.all()[:5]
    categories = Category.objects.all()
    context = {
        'latest_new':latest_new,
        'categories':categories
    }

    return context