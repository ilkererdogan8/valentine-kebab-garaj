from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from .storage import upload_to_blob, delete_from_blob


def product_list(request):
    """List all products."""
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})


def product_detail(request, pk):
    """Show a single product."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': product})


def product_create(request):
    """Create a new product."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'products/form.html', {'form': form, 'title': 'Add New Product'})


def product_update(request, pk):
    """Update an existing product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/form.html', {
        'form': form,
        'title': 'Edit Product',
        'product': product,
    })


def product_delete(request, pk):
    """Delete a product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'products/delete.html', {'product': product})
