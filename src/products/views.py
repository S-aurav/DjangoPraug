from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .forms import ProductForm, RawProductForm
from .models import Product

# Create your views here.
# def product_create_view(request):
#     myForm = RawProductForm()
#     if(request.method == "POST"):
#         myForm = RawProductForm(request.POST)
#         if myForm.is_valid():
#             # now the data is good
#             print(myForm.cleaned_data)
#             Product.objects.create(**myForm.cleaned_data)
#         else:
#             print(myForm.errors)
#     context = {
#         'form': myForm
#     }
#     return render(request, "products/product_create.html", context)

def product_create_view(request):
    initial_data = {
        'title': 'Servive'
    }
    obj = Product.objects.get(id=1)
    form = ProductForm(request.POST or None, initial=initial_data, instance=obj)
    if form.is_valid():
        form.save()
        form = ProductForm()

    context = {
        'form': form
    }
    return render(request, "products/product_create.html", context)

def product_update_view(request, id=id):
    obj = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
    
    context = {
        'form': form
    }
    return render(request, 'products/product_create.html', context)

def product_list_view(request):
    queryset = Product.objects.all() # list of objects
    context = {
        'object_list': queryset
    }

    return render(request, 'products/product_list.html', context)

def product_detail_view(request, id):
    obj = Product.objects.get(id=id)

    # context = {
    #     'title': obj.title,
    #     'description': obj.description
    # }

    context = {
        'object': obj
    }
    return render(request, "products/product_details.html", context)

def dynamic_lookup_view(request, id):
    # obj = Product.objects.get(id=my_id)
    # obj = get_list_or_404(Product, id=my_id)

    try:
        obj = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404
    
    context = {
        'object':obj
    }

    return render(request, 'products/dynamic_product.html', context)

def product_delete_view(request, id):
    obj = get_object_or_404(Product, id=id)
    #POST request
    if request.method == 'POST':
        # confirming delete
        obj.delete()
        return redirect('../../')
    
    context = {
        'object':obj
    }

    return render(request, 'products/product_delete.html', context)


