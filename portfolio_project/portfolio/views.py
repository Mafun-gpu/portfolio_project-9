from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import PortfolioItem, Category, Tag
from .forms import PortfolioItemForm
from datetime import datetime

def page_not_found(request, exception):
    """Обработчик для ошибки 404 (Страница не найдена)."""
    return render(request, 'portfolio/404.html', status=404)

def server_error(request):
    """Обработчик для ошибки 500 (Ошибка на сервере)."""
    return render(request, 'portfolio/500.html', status=500)

def permission_denied(request, exception):
    """Обработчик для ошибки 403 (Доступ запрещён)."""
    return render(request, 'portfolio/403.html', status=403)

def bad_request(request, exception):
    """Обработчик для ошибки 400 (Неверный запрос)."""
    return render(request, 'portfolio/400.html', status=400)

def portfolio_list(request):
    items = PortfolioItem.published.all().order_by('-created_at')
    return render(request, 'portfolio/index.html', {'items': items})

def save_portfolio_item_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            items = PortfolioItem.objects.all().order_by('-created_at')
            data['html_portfolio_list'] = render_to_string('portfolio/partial_portfolio_list.html', {'items': items})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def portfolio_create(request):
    if request.method == 'POST':
        form = PortfolioItemForm(request.POST, request.FILES)
    else:
        form = PortfolioItemForm()
    return save_portfolio_item_form(request, form, 'portfolio/partial_portfolio_create.html')

def portfolio_update(request, pk):
    item = get_object_or_404(PortfolioItem, pk=pk)
    if request.method == 'POST':
        form = PortfolioItemForm(request.POST, request.FILES, instance=item)
    else:
        form = PortfolioItemForm(instance=item)
    return save_portfolio_item_form(request, form, 'portfolio/partial_portfolio_update.html')

def portfolio_delete(request, pk):
    item = get_object_or_404(PortfolioItem, pk=pk)
    data = dict()
    if request.method == 'POST':
        item.delete()
        data['form_is_valid'] = True
        items = PortfolioItem.objects.all().order_by('-created_at')
        data['html_portfolio_list'] = render_to_string('portfolio/partial_portfolio_list.html', {'items': items})
    else:
        context = {'item': item}
        data['html_form'] = render_to_string('portfolio/partial_portfolio_delete.html', context, request=request)
    return JsonResponse(data)

def portfolio_detail(request, slug):
    item = get_object_or_404(PortfolioItem, slug=slug)
    return render(request, 'portfolio/portfolio_detail.html', {'item': item})

def archive_by_year(request, year):
    current_year = datetime.now().year  # получаем текущий год
    # Если переданный год больше текущего, перенаправляем на главную страницу
    if year > current_year:
        return redirect('portfolio:portfolio_list')
    
    # Фильтруем записи, созданные в указанном году
    items = PortfolioItem.objects.filter(created_at__year=year).order_by('-created_at')
    return render(request, 'portfolio/archive.html', {'year': year, 'items': items})


def category_detail(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    items = PortfolioItem.published.filter(category=category).order_by('-created_at')
    return render(request, 'portfolio/category_detail.html', {
        'category': category,
        'items': items,
    })

def tag_detail(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    items = PortfolioItem.published.filter(tags=tag).order_by('-created_at')
    return render(request, 'portfolio/tag_detail.html', {
        'tag': tag,
        'items': items,
    })