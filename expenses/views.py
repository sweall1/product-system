from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_year_month
from django.db.models import Sum


class ExpenseListView(ListView):
    model = Expense

    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        form = ExpenseSearchForm(self.request.GET)
        total_items = queryset.count()
        sum_amount = queryset.aggregate(Sum('amount'))

        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()

            if name:
                queryset = queryset.filter(name__icontains=name)

            select = form.cleaned_data['select']
            category = form.cleaned_data['category']
            if category:
                queryset = queryset.order_by('category')
            if select:
                queryset = queryset.filter(category__in=select)

            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            choice = form.cleaned_data.get("choice_field")
            grouping = form.cleaned_data['grouping']

            if grouping and choice == '1':
                queryset = queryset.order_by('date')
                queryset = queryset.filter(date__range=[start_date, end_date])
            if grouping and choice == '2':
                queryset = queryset.order_by('-date')
                queryset = queryset.filter(date__range=[start_date, end_date])

        return super().get_context_data(
            total_items=total_items,
            sum_amount=sum_amount,
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_per_year_month=summary_per_year_month(queryset),
            **kwargs)


class CategoryListView(ListView):
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        return super().get_context_data(
            object_list=queryset,
            #summary_per_year_month=summary_per_year_month(exp)
            **kwargs)




