# -*- coding: utf-8 -*-
"""Views for the customers app."""
import os, numpy
import os.path, time
import subprocess
from PIL import Image
from subprocess import check_call, Popen, PIPE
from osgeo import osr, gdal
import simplekml
import pickle
from datetime import datetime
import json

# import Image, ImageDraw
# from osgeo import gdal
# import gdal

from django.shortcuts import render
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from customers.models import (Category, ShelfData, DataSet, CustomerAccess,
                                CustomerInfoPanel, CustomerPolygons, DataPolygons,
                                AttributesReport)
from customers.customers_forms import (CategoryForm, ShelfDataForm, DataSetForm,
                                        CustomerAccessForm, CustomerPolygonsForm)
from customers.customers_update_create import (category_update_create, shelf_data_update_create,
                                                data_set_update_create, customer_access_update_create)
from core.get_post import get_post
from core.paginations import paginations
from gsi.settings import (BASE_DIR, RESULTS_DIRECTORY, GOOGLE_MAP_ZOOM,
                        POLYGONS_DIRECTORY, MEDIA_ROOT, TMP_PATH, DAFAULT_LAT,
                        DAFAULT_LON, PNG_DIRECTORY, PNG_PATH, PROJECTS_PATH,
                        KML_DIRECTORY, KML_PATH, ATTRIBUTES_NAME)


# categorys list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/categorys_list.html')
def categorys(request):
    """**View all categories for the Shelf Data.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'The categorys for the Shelf Data'
    url_name = 'categorys'
    but_name = 'info_panel'

    categorys = Category.objects.all()
    category_name = ''

    # Sorted by
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', ):
            categorys = categorys.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                categorys = categorys.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(Category, pk=int(r))
                data += '"' + cur_run.name + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(Category, pk=int(run_id))
            data = '<b>"' + cur_run.name + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('category_select'):
            for category_id in request.POST.getlist('category_select'):
                cur_category = get_object_or_404(Category, pk=category_id)
                category_name += '"' + cur_category.name + '", '
                cur_category.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('categorys_list'),
                (u'Categorys: {0} deleted.'.format(category_name))))
        elif request.POST.get('delete_button'):
            cur_category = get_object_or_404(Category, pk=request.POST.get('delete_button'))
            category_name += '"' + cur_category.name + '", '
            cur_category.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('categorys_list'), (u'Categorys: {0} deleted.'.format(category_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('categorys_list'), (u"To delete, select Category or more Categorys.")))

    # paginations
    model_name = paginations(request, categorys)

    data = {
        'title': title,
        'categorys': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# category add
@login_required
@render_to('gsi/static_data_item_edit.html')
def category_add(request):
    """**View for the "Category Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Category Add'
    url_form = 'category_add'
    template_name = 'customers/_category_form.html'
    reverse_url = {
        'save_button': 'categorys',
        'save_and_another': 'category_add',
        'save_and_continue': 'category_edit',
        'cancel_button': 'categorys'
    }
    func = category_update_create
    form = None
    url_name = 'categorys'
    but_name = 'info_panel'

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, CategoryForm, 'Category', reverse_url, func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CategoryForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'available_tiles': available_tiles,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# category edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def category_edit(request, category_id):
    """**View for the "Category "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *category_id:* The Category object ID
    """

    category = get_object_or_404(Category, pk=category_id)
    title = 'Category Edit "%s"' % (category.name)
    url_form = 'category_edit'
    template_name = 'customers/_category_form.html'
    reverse_url = {
        'save_button': 'categorys',
        'save_and_another': 'category_add',
        'save_and_continue': 'category_edit',
        'cancel_button': 'categorys'
    }
    func = category_update_create
    form = None
    url_name = 'categorys'
    but_name = 'info_panel'

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            CategoryForm,
            'Category',
            reverse_url,
            func,
            item_id=category_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CategoryForm(instance=category)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': category_id,
    }

    return data


# shelf data list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/shelf_data_list.html')
def shelf_data(request):
    """**View all Shelf Data.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'The Shelf Data'
    url_name = 'shelf_data'
    but_name = 'info_panel'

    shelf_data = ShelfData.objects.all()
    shelf_data_name = ''

    # Sorted
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('category', 'attribute_name', 'root_filename', 'units',):
            shelf_data = shelf_data.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                shelf_data = shelf_data.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(ShelfData, pk=int(r))
                data += '"' + str(cur_run) + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(ShelfData, pk=int(run_id))
            data = '<b>"' + str(cur_run) + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('shelf_data_select'):
            for shelf_data_id in request.POST.getlist('shelf_data_select'):
                cur_shelf_data = get_object_or_404(ShelfData, pk=shelf_data_id)
                shelf_data_name += '"' + cur_shelf_data.attribute_name + '", '
                cur_shelf_data.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('shelf_data_list'),
                (u'Shelf Data: {0} deleted.'.format(shelf_data_name))))
        elif request.POST.get('delete_button'):
            cur_shelf_data = get_object_or_404(ShelfData, pk=request.POST.get('delete_button'))
            shelf_data_name += '"' + cur_shelf_data.attribute_name + '", '
            cur_shelf_data.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('shelf_data_list'), (u'Shelf Data: {0} deleted.'.format(shelf_data_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('shelf_data_list'), (u"To delete, select Shelf Data or more Shelf Data.")))

    # paginations
    model_name = paginations(request, shelf_data)

    data = {
        'title': title,
        'shelf_data': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# shelf data add
@login_required
@render_to('gsi/static_data_item_edit.html')
def shelf_data_add(request):
    """**View for the "ShelfData Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Shelf Data Add'
    url_form = 'shelf_data_add'
    template_name = 'customers/_shelf_data_form.html'
    reverse_url = {
        'save_button': 'shelf_data',
        'save_and_another': 'shelf_data_add',
        'save_and_continue': 'shelf_data_edit',
        'cancel_button': 'shelf_data'
    }
    func = shelf_data_update_create
    form = None
    url_name = 'shelf_data'
    but_name = 'info_panel'
    available_tiles = ShelfData.objects.all()

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, ShelfDataForm, 'Shelf Data', reverse_url, func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = ShelfDataForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'available_tiles': available_tiles,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# shelf data edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def shelf_data_edit(request, shelf_data_id):
    """**View for the "ShelfData "<attribute_name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *shelf_data_id:* The ShelfData object ID
    """

    shelf_data = get_object_or_404(ShelfData, pk=shelf_data_id)
    title = 'Category Edit "%s"' % (shelf_data.attribute_name)
    url_form = 'shelf_data_edit'
    template_name = 'customers/_shelf_data_form.html'
    reverse_url = {
        'save_button': 'shelf_data',
        'save_and_another': 'shelf_data_add',
        'save_and_continue': 'shelf_data_edit',
        'cancel_button': 'shelf_data'
    }
    func = shelf_data_update_create
    form = None
    url_name = 'shelf_data'
    but_name = 'info_panel'

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            ShelfDataForm,
            'Shelf Data',
            reverse_url,
            func,
            item_id=shelf_data_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = ShelfDataForm(instance=shelf_data)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': shelf_data_id,
    }

    return data


# data sets list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/dataset_list.html')
def data_sets(request):
    """**View all the DataSets.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'DataSets Definition'
    url_name = 'data_sets'
    but_name = 'info_panel'

    data_sets = DataSet.objects.all()
    data_set_name = ''

    # Sorted by name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', 'description', 'results_directory', 'shelf_data__attribute_name', 'shelf_data__root_filename'):
            data_sets = data_sets.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                data_sets = data_sets.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(DataSet, pk=int(r))
                data += '"' + cur_run.name + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(DataSet, pk=int(run_id))
            data = '<b>"' + cur_run.name + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('dataset_select'):
            for data_set_id in request.POST.getlist('dataset_select'):
                cur_data_set = get_object_or_404(DataSet, pk=data_set_id)
                data_set_name += '"' + cur_data_set.name + '", '
                cur_data_set.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('data_sets'),
                (u'DataSets: {0} deleted.'.format(data_set_name))))
        elif request.POST.get('delete_button'):
            cur_data_set = get_object_or_404(DataSet, pk=request.POST.get('delete_button'))
            data_set_name += '"' + cur_data_set.name + '", '
            cur_data_set.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('data_sets'), (u'DataSets: {0} deleted.'.format(data_set_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('data_sets'), (u"To delete, select DataSet or more DataSets.")))

    # paginations
    model_name = paginations(request, data_sets)

    data = {
        'title': title,
        'data_sets': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# shelf data add
@login_required
@render_to('gsi/static_data_item_edit.html')
def data_set_add(request):
    """**View for the "DataSet Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'DataSet Add'
    url_form = 'data_set_add'
    template_name = 'customers/_data_set_form.html'
    reverse_url = {
        'save_button': 'data_sets',
        'save_and_another': 'data_set_add',
        'save_and_continue': 'data_set_edit',
        'cancel_button': 'data_sets'
    }
    func = data_set_update_create
    form = None
    shelf_data = ShelfData.objects.all()
    url_name = 'data_sets'
    but_name = 'info_panel'
    dirs_list = []

    # Ajax when insert the root_filename and the attribute_name
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'shelf_data_id' in data_post:
            shelf_data_id = data_post['shelf_data_id']
            shelf_data = get_object_or_404(ShelfData, pk=int(shelf_data_id))
            root_filename = shelf_data.root_filename
            attribute_name = shelf_data.attribute_name
            data = root_filename + '$$$' + attribute_name

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)


    # Handling POST request
    if request.method == "POST":
        if request.POST.get('update_button') is not None:
            form = DataSetForm(request.POST)

            if form.is_valid():
                if form.cleaned_data['results_directory']:
                    try:
                        results_directory = RESULTS_DIRECTORY + form.cleaned_data['results_directory']
                        root, dirs, files = os.walk(results_directory).next()

                        for sd in shelf_data:
                            if str(sd.root_filename) in dirs:
                                dirs_list.append(sd)
                    except StopIteration:
                        return HttpResponseRedirect(
                            u'%s?danger_message=%s' % (reverse('data_set_add'),
                            (u'The directory "{0}" does not exist!'.format(results_directory)))
                        )
        else:
            response = get_post(request, DataSetForm, 'DataSet', reverse_url, func)

            if isinstance(response, HttpResponseRedirect):
                return response
            else:
                form = response
    else:
        form = DataSetForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'url_name': url_name,
        'but_name': but_name,
        'dirs_list': dirs_list,
    }

    return data


# shelf data edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def data_set_edit(request, data_set_id):
    """**View for the "DataSets "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *data_set_id:* The ShelfData object ID
    """

    data_set = get_object_or_404(DataSet, pk=data_set_id)
    title = 'DataSet Edit "%s"' % (data_set.name)
    url_form = 'data_set_edit'
    template_name = 'customers/_data_set_form.html'
    reverse_url = {
        'save_button': 'data_sets',
        'save_and_another': 'data_set_add',
        'save_and_continue': 'data_set_edit',
        'cancel_button': 'data_sets'
    }
    func = data_set_update_create
    form = None
    shelf_data = ShelfData.objects.all()
    url_name = 'data_sets'
    but_name = 'info_panel'
    dirs_list = []

    # Get the results_directorys list
    try:
        results_directory = RESULTS_DIRECTORY + data_set.results_directory
        root, dirs, files = os.walk(results_directory).next()

        for sd in shelf_data:
            if str(sd.root_filename) in dirs:
                dirs_list.append(sd)
    except Exception:
        pass

    # Ajax when insert the root_filename and the attribute_name
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'shelf_data_id' in data_post:
            shelf_data_id = data_post['shelf_data_id']
            shelf_data = get_object_or_404(ShelfData, pk=int(shelf_data_id))
            root_filename = shelf_data.root_filename
            attribute_name = shelf_data.attribute_name
            data = root_filename + '$$$' + attribute_name

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        # Update the results_directorys list
        if request.POST.get('update_button') is not None:
            form = DataSetForm(request.POST)
            dirs_list = []

            if form.is_valid():
                if form.cleaned_data['results_directory']:
                    results_directory = RESULTS_DIRECTORY + form.cleaned_data['results_directory']

                    try:
                        root, dirs, files = os.walk(results_directory).next()

                        for sd in shelf_data:
                            if str(sd.root_filename) in dirs:
                                dirs_list.append(sd)
                    except StopIteration:
                        return HttpResponseRedirect(
                            u'%s?danger_message=%s' % (reverse('data_set_edit', args=[data_set_id]),
                            (u'The directory "{0}" does not exist!'.format(results_directory)))
                        )
        else:
            response = get_post(request, DataSetForm, 'DataSet', reverse_url, func, item_id=data_set_id)

            if isinstance(response, HttpResponseRedirect):
                return response
            else:
                form = response
    else:
        form = DataSetForm(instance=data_set)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': data_set_id,
        'data_set': data_set,
        'dirs_list': dirs_list,
    }

    return data


# customers access list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/customer_access_list.html')
def customer_access(request):
    """**View the Customer Access.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'Customer Access'
    url_name = 'customer_access'
    but_name = 'info_panel'

    customers_access = CustomerAccess.objects.all()
    customer_access_name = ''

    # Sorted by customer name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('user', ):
            customers_access = customers_access.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                customers_access = customers_access.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(CustomerAccess, pk=int(r))
                data += '"{0}", '.format(cur_run)

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(CustomerAccess, pk=int(run_id))
            data = '<b>"{0}"</b>'.format(cur_run)
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('customer_access_select'):
            for customer_access_id in request.POST.getlist('customer_access_select'):
                cur_customer_access = get_object_or_404(CustomerAccess, pk=customer_access_id)
                customer_access_name += '"{0}", '.format(cur_customer_access)
                cur_customer_access.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('customer_access'),
                (u'Customers Access: {0} deleted.'.format(customer_access_name))))
        elif request.POST.get('delete_button'):
            cur_customer_access = get_object_or_404(CustomerAccess, pk=request.POST.get('delete_button'))
            customer_access_name += '"{0}", '.format(cur_customer_access)
            cur_customer_access.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('customer_access'), (u'Customers Access: {0} deleted.'.format(customer_access_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('customer_access'), (u"To delete, select Customer Access or more Customers Access.")))

    # paginations
    model_name = paginations(request, customers_access)

    data = {
        'title': title,
        'customers_access': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# customer access add
@login_required
@render_to('gsi/static_data_item_edit.html')
def customer_access_add(request):
    """**View for the "Customer Access Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Customer Access Add'
    url_form = 'customer_access_add'
    template_name = 'customers/_customer_access_form.html'
    reverse_url = {
        'save_button': 'customer_access',
        'save_and_another': 'customer_access_add',
        'save_and_continue': 'customer_access_edit',
        'cancel_button': 'customer_access'
    }
    func = customer_access_update_create
    form = None
    url_name = 'customer_access'
    but_name = 'info_panel'
    available_data_set = DataSet.objects.all()

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, CustomerAccessForm, 'Customer Access', reverse_url, func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CustomerAccessForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'available_data_set': available_data_set,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# customer access edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def customer_access_edit(request, customer_access_id):
    """**View for the "Customer Access "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *customer_access_id:* The CustomerAccess object ID
    """

    customer_access = get_object_or_404(CustomerAccess, pk=customer_access_id)
    title = 'Customer Access Edit "%s"' % (customer_access)
    url_form = 'customer_access_edit'
    template_name = 'customers/_customer_access_form.html'
    reverse_url = {
        'save_button': 'customer_access',
        'save_and_another': 'customer_access_add',
        'save_and_continue': 'customer_access_edit',
        'cancel_button': 'customer_access'
    }
    func = customer_access_update_create
    form = None
    url_name = 'customer_access'
    but_name = 'info_panel'
    chosen_data_set = customer_access.data_set.all()
    available_data_set = DataSet.objects.exclude(id__in=customer_access.data_set.values_list('id', flat=True))

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request, CustomerAccessForm, 'Customer Access', reverse_url, func, item_id=customer_access_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CustomerAccessForm(instance=customer_access)

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'item_id': customer_access_id,
        'available_data_set': available_data_set,
        'chosen_data_set': chosen_data_set,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


def remove_file_png(file_path):
    # Get the png file for the delete
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception, e:
        print 'Exception remove file png ========================= ', e


def check_current_dataset(request, data_post):
    is_delete = False
    data_set_id = data_post.get('datasets_id', '')
    request.session['select_data_set'] = data_set_id
    data_set = DataSet.objects.get(pk=data_set_id)

    # print 'data_set_id ==================================', request.session['select_data_set']

    if not CustomerInfoPanel.objects.filter(user=request.user, data_set=data_set).exists():
        info_panel = CustomerInfoPanel.objects.filter(user=request.user).delete()
        is_delete = True
        
    return is_delete


def check_date_files(file_tif, file_png):
    try:
        f_tif = os.path.getmtime(file_tif)
        f_png = os.path.getmtime(file_png)

        if f_tif > f_png:
            return True
    except Exception, e:
        print 'Exception check_date_files ========================= ', e
        return True

    return False


ATTRIBUTE_NAMES = [
    'mean_ConditionalMax',
    'mean_ConditionalMean',
    'mean_ConditionalMedian',
    'mean_ConditionalMin',
    'mean_LowerQuartile',
    'mean_Quantile'
]


def checkKmlFile(filename):
    kml_filename = filename + '.kml'
    file_path = os.path.join(KML_PATH, kml_filename)
    
    if os.path.exists(file_path):
        for n in xrange(1000000):
            fn = filename + '_' + str(n)
            kml_filename = fn + '.kml'
            file_path = os.path.join(KML_PATH, kml_filename)
            
            if not os.path.exists(file_path):
                filename = fn
                break
                
    return filename
    
    
def getIndex(stroke):
    index = stroke.split('[')
    index = index[1].split(']')
    index = int(index[0])
    
    return index
    
    
def getGeoCoord(filename):
    coord = []
    f = open(filename)
    
    for line in f.readlines():
        line = line.rstrip('\n')
        line = line.split(',')
        tmp = [float(line[0]), float(line[1])]
        coord.append(tmp)
        
    return coord
    
    
def addPolygonToDB(name, kml_name, user, kml_path, kml_url, ds):
    customer_pol = CustomerPolygons.objects.none()
    
    if CustomerPolygons.objects.filter(name=name).exists():
        CustomerPolygons.objects.filter(name=name).update(
            name=name,
            kml_name=kml_name,
            user=user,
            data_set=ds,
            kml_path=kml_path,
            kml_url=kml_url
        )
        customer_pol = CustomerPolygons.objects.get(
                            name=name,
                            kml_name=kml_name,
                            user=user,
                            data_set=ds,
                            kml_path=kml_path,
                            kml_url=kml_url
                        )
    else:
        customer_pol = CustomerPolygons.objects.create(
                            name=name,
                            kml_name=kml_name,
                            user=user,
                            data_set=ds,
                            kml_path=kml_path,
                            kml_url=kml_url
                        )
                        
    return customer_pol
    
    
def get_parameters_customer_info_panel(data_set, shelf_data, stat_file, absolute_png_url):
    # print 'data_set =========================== ', data_set
    # order_data_set = data_set.order_by('attribute_name')
    attribute_name = shelf_data.attribute_name
    results_directory = data_set.results_directory
    project_name = results_directory.split('/')[0]
    file_area_name = '{0}_{1}.{2}'.format(stat_file, shelf_data.root_filename, project_name)
    tif = '{0}.tif'.format(file_area_name)
    png = '{0}.png'.format(file_area_name)
    tif_path = os.path.join(PROJECTS_PATH, data_set.results_directory, shelf_data.root_filename, tif)
    png_path = os.path.join(PNG_PATH, png)
    url_png = '{0}/{1}'.format(absolute_png_url, png)
    
    return attribute_name, file_area_name, tif_path, png_path, url_png
    
def createCustomerInfoPanel(customer, data_set, shelf_data, stat_file, absolute_png_url,
                            is_show, order=0, delete=True):
    if delete:
        CustomerInfoPanel.objects.filter(user=customer).delete()
        
    attribute_name, file_area_name,\
    tif_path, png_path, url_png = get_parameters_customer_info_panel(data_set,
                                    shelf_data, stat_file, absolute_png_url)
                                        
    info_panel = CustomerInfoPanel.objects.create(
                    user=customer,
                    data_set=data_set,
                    attribute_name=attribute_name,
                    statisctic=stat_file,
                    file_area_name=file_area_name,
                    tif_path=tif_path,
                    png_path=png_path,
                    url_png=url_png,
                    order=order,
                    is_show=is_show)
    info_panel.save()
    
    return info_panel
    
    
def createKml(user, filename, info_window, url, data_set):
    # Create KML file for the draw polygon
    kml_filename = str(filename) + '.kml'
    tmp_file = str(user) + '_coord_tmp.txt'
    tmp_path = os.path.join(KML_PATH, tmp_file)
    coord = getGeoCoord(tmp_path)
    kml_url = url + '/' + kml_filename
    
    # print 'coord ========================== ', coord
    
    kml = simplekml.Kml()
    pol = kml.newpolygon(name=filename)
    pol.outerboundaryis.coords = coord
    pol.style.linestyle.color = simplekml.Color.hex('#ffffff')
    pol.style.linestyle.width = 5
    pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.hex('#8bc53f'))
    
    pol.style.balloonstyle.text = info_window
    pol.style.balloonstyle.bgcolor = simplekml.Color.lightgreen
    pol.style.balloonstyle.textcolor = simplekml.Color.hex('#283890')

    kml_path = os.path.join(KML_PATH, kml_filename)
    kml.save(kml_path)
    
    polygon = addPolygonToDB(filename, kml_filename, user, kml_path, kml_url, data_set)
    
    return polygon
    
    
def getAttributeUnits(user, show_file):
    attribute_name = 'Tree Count'
    units = '%'
    
    try:
        cur_attribute = CustomerInfoPanel.objects.get(
                            user=user,
                            file_area_name=show_file)
        attribute_name = cur_attribute.attribute_name
        sh_data = ShelfData.objects.filter(attribute_name=attribute_name)
        units = sh_data[0].units
    except Exception:
        pass
    
    return attribute_name, units
    
    
def getResultDirectory(dataset, shelfdata):
    dirs_list = []
    
    try:
        project_directory = os.path.join(PROJECTS_PATH, dataset.results_directory)
        root, dirs, files = os.walk(project_directory).next()
        dirs.sort()
        
        for sd in shelfdata:
            if str(sd.root_filename) in dirs:
                dirs_list.append(sd)
    except Exception, e:
        print 'Exception getResultDirectory ========================= ', e
        pass
        
    return dirs_list
    
    
def getDataSet(ds_id, data_set):
    data_set_id = ds_id
    
    try:
        data_set = DataSet.objects.get(pk=data_set_id)
    except DataSet.DoesNotExist, e:
        print 'DataSet.DoesNotExist ========================= ', e
        data_set_id = int(data_set.id)
        
    return data_set, data_set_id

# view Customer Section
@login_required
@render_to('customers/customer_section.html')
def customer_section(request):
    """**View for the "Customer section" page.**

    :Functions:
        When you load the page is loaded map with Google MAP. Initial coordinates: eLat = 0, eLng = 0.
        Zoom map is variable GOOGLE_MAP_ZOOM, whose value is in the project settings.
        Code view allows to change position when you enter values in the fields on the page "Enter Lat" and "Enter Log".

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    # PNG_DIRECTORY = 'media/png'
    # PNG_PATH = os.path.join(BASE_DIR, PNG_DIRECTORY)
    # PROJECTS_PATH = '/lustre/w23/mattgsi/satdata/RF/Projects'

    customer = request.user
    shelf_data_all = ShelfData.objects.all().order_by('attribute_name')
    # customer_info_panel = CustomerInfoPanel.objects.filter(user=customer)
    customer_polygons = CustomerPolygons.objects.filter(user=customer)
    polygons_path = os.path.join(MEDIA_ROOT, 'kml')
    customer_access = CustomerAccess.objects.get(user=customer)
    customer_access_ds = CustomerAccess.data_set.through.objects.filter(
                    customeraccess_id=customer_access.id).order_by('dataset_id')
                    
    url_name = 'customer_section'
    data_sets = []
    error_message = ''
    warning_message = ''
    data_set_id = 0
    polygons = []
    attribute_list_infopanel = []
    statisctics_infopanel = []
    show_dataset_cip = ''
    show_image_cip = ''
    show_statistic_cip = ''
    show_report_ap = []
    file_tif_path = ''
    tab_active = 'view'
    # current_area_image = ''
    
    # default GEOTIFF coordinates
    cLng = DAFAULT_LON
    cLat = DAFAULT_LAT
    eLat_1 = 0
    eLng_1 = 0
    eLat_2 = 0
    eLng_2 = 0
    google_map_zoom = 6
    url_png = ''
    
    # The path to are PNG, KML urls
    scheme = '{0}://'.format(request.scheme)
    absolute_png_url = os.path.join(scheme, request.get_host(), PNG_DIRECTORY)
    absolute_kml_url = os.path.join(scheme, request.get_host(), KML_DIRECTORY)
    
    # Get the User DataSets
    if customer_access_ds:
        for n in customer_access_ds:
            try:
                ds = DataSet.objects.get(pk=n.dataset_id)
                data_sets.append(ds)
            except DataSet.DoesNotExist, e:
                print 'ERROR Get DataSet ==================== ', e
                pass
    else:
        error_message = 'You have no one DataSet for view. Please contact to the admin.'
        data = {
            'error_message': error_message
        }
        
        return data
        
    # GET SESSIONS !!!!!!!!!!!!!!!!!!!!!!!!!
    # Get select data_set sessions
    if request.session.get('select_data_set', False):
        data_set_id = int(request.session['select_data_set'])
    else:
        CustomerInfoPanel.objects.filter(user=customer).delete()
        request.session['select_data_set'] = data_sets[0].id
        # request.session.set_expiry(172800)
    
    # Get select active tab sessions
    if request.session.get('tab_active', False):
        tab_active = request.session['tab_active']
    else:
        request.session['tab_active'] = tab_active
        
    # Get the DataSet and DataSet ID select
    data_set, data_set_id = getDataSet(data_set_id, data_sets[0])

    # Get the Statistics list
    dirs_list = getResultDirectory(data_set, shelf_data_all)
        
    # get AJAX POST for KML files
    if request.is_ajax() and request.method == "POST":
        data_post_ajax = request.POST
        data = ''
        
        print '!!!!!!!!!!!!!!!!! data_post_ajax ===================== ', data_post_ajax
        # print '!!!!!!!!!!!!!!!!! data_post_ajax LIST ===================== ', data_post_ajax.lists()
        # print '!!!!!!!!!!!!!!!!! coordinate_list[0][] ===================== ', 'coordinate_list[0][]' in data_post_ajax
        # print '!!!!!!!!!!!!!!!!! BUTTON ===================== ', 'button' in data_post_ajax
        
        
        if 'button' in data_post_ajax:
            if 'attr_list[]' in data_post_ajax and 'stat_list[]' in data_post_ajax:
                attributes_viewlist = data_post_ajax.getlist('attr_list[]')
                statistics_viewlist = data_post_ajax.getlist('stat_list[]')
                
                # print 'attributes_viewlist ========================= ', attributes_viewlist
                # print 'statistics_viewlist ========================= ', statistics_viewlist
                
                count_obj = len(attributes_viewlist) * len(statistics_viewlist) - 1
                is_show = False
                new_order = 0
                show_order = 0
                show_attribute_name = ''
                show_statistics_name = ''
                is_show_sip = CustomerInfoPanel.objects.filter(
                                user=customer, is_show=True)
                                
                if is_show_sip:
                    show_attribute_name = is_show_sip[0].attribute_name
                    show_statistics_name = is_show_sip[0].statisctic
                
                # print 'CIP count_obj ========================= ', count_obj
                # print 'CIP ORDER ========================= ', is_show_sip[0].order
                # print 'show_statistics_name ========================= ', show_statistics_name
                
                CustomerInfoPanel.objects.filter(user=customer).delete()
                
                for attr in attributes_viewlist:
                    attr_id = int(attr.split('view_')[1])
                    
                    try:
                        shelf_data = ShelfData.objects.get(id=int(attr_id))
                        
                        for st in statistics_viewlist:
                            createCustomerInfoPanel(customer, data_set, shelf_data,
                                                    st, absolute_png_url,
                                                    False, order=new_order, delete=False)
                            
                            
                            if show_attribute_name == shelf_data.attribute_name and show_statistics_name == st:
                                if data_post_ajax['button'] == 'next':
                                    show_order = new_order + 1
                                elif data_post_ajax['button'] == 'previous':
                                    show_order = new_order - 1
                            
                            new_order += 1
                            # print '**************************************************************************************'
                            # print 'show_attribute_name ========================= ', show_attribute_name
                            # print 'shelf_data.attribute_name ========================= ', shelf_data.attribute_name
                            # print ''
                            # print 'show_statistics_name ========================= ', show_statistics_name
                            # print 'statistics ========================= ', st
                            # print '!!!!!!!!!!!!! show_order ========================= ', show_order
                            # print '**************************************************************************************'
                    except ShelfData.DoesNotExist:
                        pass
                        
                if is_show_sip:
                    if show_order > count_obj:
                        show_order = 0
                    elif show_order < 0:
                        show_order = count_obj
                    CustomerInfoPanel.objects.filter(user=customer, order=show_order).update(is_show=True)
                else:
                    CustomerInfoPanel.objects.filter(user=customer, order=0).update(is_show=True)
                    
                # try:
                #     show_cip = CustomerInfoPanel.objects.get(user=customer, is_show=True)
                #     data = '{0}${1}${2}'.format(show_cip.data_set.name, show_cip.attribute_name, show_cip.statisctic)
                # except CustomerInfoPanel.DoesNotExist:
                #     pass
                
                return HttpResponse(data)
            elif 'attr_list[]' in data_post_ajax or not 'stat_list[]' in data_post_ajax:
                createCustomerInfoPanel(customer, data_set, dirs_list[0],
                                        'mean_ConditionalMean', absolute_png_url,
                                        True, order=0)
                
            return HttpResponse(data)
    
        if 'coordinate_list[0][]' in data_post_ajax:
            reports_cip = []
            statistic = ''
            
            if 'reports[]' in data_post_ajax:
                reports_ids = []
                for rep_id in data_post_ajax.getlist('reports[]'):
                    reports_ids.append(rep_id.split('report_')[1])
                    
                reports_cip = ShelfData.objects.filter(
                                id__in=reports_ids).order_by('attribute_name')
            else:
                reports_cip = dirs_list
                
            if 'stats[]' in data_post_ajax:
                for stat in data_post_ajax.getlist('stats[]'):
                    statistic = stat
            
            # print '!!!!!!!!!!!!! statistic ====================== ', statistic
            # print '!!!!!!!!!!!!! statistic TYPE ====================== ', type(statistic)
                
            AttributesReport.objects.filter(user=customer).delete()
            cips = CustomerInfoPanel.objects.filter(user=customer)
            
            for cip in cips:
                cip.statisctic = statistic
                cip.save()
                
            for rs in reports_cip:
                attribute_report = AttributesReport.objects.create(
                                        user=customer,
                                        data_set=data_set,
                                        shelfdata=rs,
                                        statisctic=statistic
                                    )
                                
            coord_tmp = str(request.user) + '_coord_tmp.txt'
            php_tmp = str(request.user) + '_php_tmp.txt'
            file_path_coord = os.path.join(KML_PATH, coord_tmp)
            file_path_php = os.path.join(KML_PATH, php_tmp)
            myfile_coord = open(file_path_coord, "w")
            myfile_php = open(file_path_php, "w")
            
            list_size = len(data_post_ajax.lists()) - 1
            coord = []*list_size
            tmp = {}
            coord_dict = {}
            lon = []
            lat = []
            
            for n in data_post_ajax.lists():
                if n[0] != 'csrfmiddlewaretoken' and n[0] != 'reports[]' and n[0] != 'stats[]':
                    index = getIndex(n[0])
                    tmp[index] = n[1]

            for k in sorted(tmp.keys()):
                coord_dict[k] = tmp[k]
                
            for n in coord_dict:
                myfile_coord.write(",".join(coord_dict[n]));
                myfile_coord.write("\n");
                
            for n in coord_dict:
                lon.append(coord_dict[n][0])
                lat.append(coord_dict[n][1])
                
            lat_str = ','.join(lat)
            lon_str = ','.join(lon)
            
            # print '!!!!!!!!!!!!!!!! lat_str =========================== ', lat_str
            # print '!!!!!!!!!!!!!!!! lat_str =========================== ', lat_str
            
            myfile_php.write(lat_str);
            myfile_php.write("\n");
            myfile_php.write(lon_str);
            myfile_php.write("\n");
            
            myfile_coord.close()
            myfile_php.close()
            
            # print 'coord_dict ======================== ', coord_dict

            return HttpResponse(data)
            
        if 'cur_run_id' in data_post_ajax:
            # message = u'Are you sure you want to remove this objects:'
            arrea = data_post_ajax['cur_run_id']
            data = u'Are you sure you want to remove this objects: <b>"{0}"</b>?'.format(arrea)

            return HttpResponse(data)
        else:
            return HttpResponse(data)
    
    
    # get AJAX GET
    if request.is_ajax() and request.method == "GET":
        data = ''
        data_get_ajax = request.GET
        cip = CustomerInfoPanel.objects.filter(user=customer)
        
        print 'GET customer_section ====================== ', data_get_ajax
        
        # When user celect a new DataSet, the previous celected DataSet to remove
        if 'datasets_id' in data_get_ajax:
            for ip in cip:
                remove_file_png(ip.png_path)

            status = check_current_dataset(request, data_get_ajax)
            
            if request.session.get('select_data_set', False):
                data_set_id = int(request.session['select_data_set'])
            else:
                request.session['select_data_set'] = data_sets[0].id
                data_set_id = request.session['select_data_set']
            
            # print 'data_set_id REQ ========================== ', request.session['select_data_set']
            # print 'data_set_id ========================== ', data_set_id
            
            if status:
                data_set, data_set_id = getDataSet(data_set_id, data_sets[0])
                dirs_list = getResultDirectory(data_set, shelf_data_all)
                statisctic = 'mean_ConditionalMean'
                is_show = True
                
                # print 'data_set ========================== ', data_set
                # print 'dirs_list[0] ========================== ', dirs_list[0]
                if dirs_list:
                    info_panel = createCustomerInfoPanel(
                                    customer, data_set, dirs_list[0], statisctic,
                                    absolute_png_url, is_show
                                )
                else:
                    data = 'error'
                    # print 'ERRRRRRRRRRRRRRRRRRRRRRRROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                    
        if 'cur_area' in data_get_ajax:
            # print 'POL ========================================= ', data_get_ajax.get('cur_area', '')
            polygon_id = data_get_ajax.get('cur_area', '')
            try:
                select_area = CustomerPolygons.objects.get(pk=polygon_id)
                data = '{0}${1}'.format(select_area.name, polygon_id)
            except CustomerPolygons.DoesNotExist:
                data = 'There is no such polygon.'
                
        if 'polygon' in data_get_ajax:
            # for ip in cip:
            #     remove_file_png(ip.png_path)
            #
            # CustomerInfoPanel.objects.filter(user=request.user).delete()
            
            polygon = data_get_ajax.get('polygon', '')
            data = os.path.join(absolute_kml_url, polygon)
                
        if 'tab_active' in data_get_ajax:
            tab_active = data_get_ajax.get('tab_active', '')
            request.session['tab_active'] = tab_active
            # print 'tab_active ================================ ', tab_active
            
        return HttpResponse(data)
    
    if request.method == "POST":
        data_post = request.POST
        # print 'POST =========================== ', data_post
    
        if 'save_area' in data_post:
            data_kml = data_post.lists()
            area_name = ''
            total_area = ''
            attribute = []
            value = []
            units = []
            total = []
            statistic = ''
                    
            for item in data_kml:
                # total_area
                if 'total_area' in item:
                    total_area = item[1][0]
                    
                if 'area_name' in item:
                    area_name = item[1][0].replace(' ', '-')
                    
                if 'attribute' in item:
                    attribute = item[1]
                    
                if 'value' in item:
                    value = item[1]
                    
                if 'units' in item:
                    units = item[1]
                    
                if 'total' in item:
                    total = item[1]
                    
                if 'statistic' in item:
                    statistic = item[1][0]
                    
            len_attr = len(attribute)
            
            info_window = '<h4 align="center">Attribute report: {0}</h4>\n'.format(area_name)
            info_window += '<p align="center"><span><b>Total Area:</b></span> ' + total_area + ' ha</p>';
            
            if statistic:
                info_window += '<p align="center"><span><b>Values:</b></span> ' + statistic + ' ha</p>';
            # info_window += '<p align="left"><font size="2">{0}: {1} ha</p></font>\n'.format(ATTRIBUTES_NAME[0], total_area)
            
            if len_attr >= 8:
                info_window += '<div style="height:400px;overflow:scroll;">'
            else:
                info_window += '<div style="overflow:auto;">'
            
            info_window += '<table border="1" cellspacing="5" cellpadding="5" style="border-collapse:collapse;border:1px solid black;width:100%;">\n'
            # info_window += '<caption align="left" style="margin-bottom:15px"><span><b>Total Area:</b></span> ' + total_area + ' ha</caption>'
            info_window += '<thead>\n'
            info_window += '<tr bgcolor="#CFCFCF">\n'
            info_window += '<th align="left" style="padding:10px">Attribute</th>\n'
            info_window += '<th style="padding:10px">Value</th>\n'
            info_window += '<th style="padding:10px">Units</th>\n'
            info_window += '<th style="padding:10px">Total</th>\n'
            info_window += '</tr>\n'
            info_window += '</thead>\n'
            info_window += '<tbody>\n'
            
            for n in xrange(len_attr):
                if n % 2 == 0:
                    info_window += '<tr bgcolor="#F5F5F5">\n'
                else:
                    info_window += '<tr>';
                    
                info_window += '<td align="left" style="padding:10px">{0}</td>\n'.format(attribute[n])
                info_window += '<td style="padding:10px">{0}</td>\n'.format(value[n])
                info_window += '<td style="padding:10px">{0}</td>\n'.format(units[n])
                info_window += '<td style="padding:10px">{0}</td>\n'.format(total[n])
                info_window += '</tr>\n'
            
            info_window += '</tbody>\n'
            info_window += '</table>\n'
            info_window += '</div>'
                
            # Create KML file for the draw polygon
            ds = DataSet.objects.get(pk=data_set_id)
            cur_polygon = createKml(request.user, area_name, info_window, absolute_kml_url, ds)
            
            for n in xrange(len_attr):
                if not DataPolygons.objects.filter(user=request.user, data_set=data_set,
                    customer_polygons=cur_polygon, attribute=attribute[n]).exists():
                        DataPolygons.objects.create(
                            user=request.user,
                            customer_polygons=cur_polygon,
                            data_set=data_set,
                            attribute=attribute[n],
                            value=value[n],
                            units=units[n],
                            total=total[n],
                            total_area=total_area+' ha'
                        )
                elif DataPolygons.objects.filter(user=request.user, data_set=data_set,
                    customer_polygons=cur_polygon, attribute=attribute[n]).exists():
                        DataPolygons.objects.filter(
                            customer_polygons=cur_polygon, attribute=attribute[n]
                        ).update(
                            # attribute=attribute[n],
                            value=value[n],
                            units=units[n],
                            total=total[n],
                            total_area=total_area+' ha'
                        )
                        
        if 'delete_button' in data_post:
            kml_file = data_post.get('delete_button')
            
            # print 'kml_file ======================================== ', kml_file
            cur_area = get_object_or_404(
                CustomerPolygons, kml_name=kml_file)
            os.remove(cur_area.kml_path)
            cur_area.delete()
            cur_data_polygons = DataPolygons.objects.filter(
                                    customer_polygons=cur_area
                                )
            for data_pol in cur_data_polygons:
                data_pol.delete()
        
            return HttpResponseRedirect(u'%s' % (reverse('customer_section')))
                    
        if 'area_name' in data_post:
            area_id = data_post.get('save_area_name', '')
        
            if area_id:
                old_area = CustomerPolygons.objects.get(pk=area_id)
                new_area_name = data_post.get('area_name')
                new_area_name = new_area_name.replace(' ', '-')
                new_kml_name = str(new_area_name) + '.kml'
                old_path = old_area.kml_path
                new_path = os.path.join(KML_PATH, new_kml_name)
        
                os.rename(old_path, new_path)
        
                area = CustomerPolygons.objects.filter(pk=area_id).update(
                            name = new_area_name,
                            kml_name = new_kml_name,
                            kml_path = new_path)
        
                return HttpResponseRedirect(u'%s' % (reverse('customer_section')))
    
    
    
    customer_info_panel = CustomerInfoPanel.objects.filter(user=customer)
    
    # if not customer_info_panel and dirs_list:
    #     attribute_list_infopanel.append(dirs_list[0].attribute_name)
    #     statisctics_infopanel.append('mean_ConditionalMean')
    #     current_area_image = ''
    if customer_info_panel and dirs_list:
        cip = customer_info_panel.filter(user=customer).order_by('attribute_name')
        
        for n in cip:
            attribute_list_infopanel.append(n.attribute_name)
            statisctics_infopanel.append(n.statisctic)
        
    
    # Get the polygons list from media folder
    polygons = CustomerPolygons.objects.filter(
                    user=request.user,
                    data_set=data_set
                )
    
    # print 'shelf_data_all ======================================= ', shelf_data_all
    # print '!!!!!!!! dirs_list ======================================= ', dirs_list
    # attribute_list_infopanel
    # print '!!!!!!!! attribute_list_infopanel ======================================= ', attribute_list_infopanel
    # print 'statisctics_infopanel ======================================= ', statisctics_infopanel
    
    if customer_info_panel:
        try:
            customer_info_panel_file = CustomerInfoPanel.objects.filter(
                                        user=request.user,
                                        is_show=True)
                                        
            if customer_info_panel_file:
                file_tif = customer_info_panel_file[0].tif_path
                file_png = customer_info_panel_file[0].png_path
                url_png = customer_info_panel_file[0].url_png
                
                ####################### write log file
                # log_file = '/home/gsi/LOGS/customer_section.log'
                # customer_section = open(log_file, 'a+')
                # now = datetime.now()
                # customer_section.write('USER: '+str(request.user))
                # customer_section.write('\n')
                # customer_section.write('DATA SET: '+str(data_set))
                # customer_section.write('\n')
                # customer_section.write('FILE AREA NAME: '+str(show_file))
                # customer_section.write('\n')
                # customer_section.write('CUSTOMER INFO PANEL: '+str(customer_info_panel_file))
                # customer_section.write('\n')
                #
                # customer_section.close()
                #######################

                # Convert tif to png

                # Set file vars
                # # output_file = "out.jpg"
                # # output_file_root = os.path.splitext(output_file)[0]
                # output_file_ext = 'png'
                # output_file_tmp = customer_info_panel_file.file_area_name + ".tmp"
                #
                # # Create tmp gtif
                # driver = gdal.GetDriverByName("GTiff")
                # dst_ds = driver.Create(output_file_tmp, 512, 512, 1, gdal.GDT_Byte )
                # raster = numpy.zeros( (512, 512) )
                # dst_ds.GetRasterBand(1).WriteArray(raster)
                #
                # # Create jpeg or rename tmp file
                # if (cmp(output_file_ext.lower(),"png" ) == 0):
                #     jpg_driver = gdal.GetDriverByName("PNG")
                #     jpg_driver.CreateCopy( file_png, dst_ds, 0 )
                #     os.remove(output_file_tmp)
                # else:
                #     os.rename(output_file_tmp, file_png)

                try:
                    check_date = check_date_files(file_tif, file_png)

                    if check_date:
                        if os.path.exists(file_tif):
                            proc = Popen(['cat', file_tif], stdout=PIPE)
                            p2 = Popen(['convert', '-', file_png], stdin=proc.stdout)

                            while not os.path.exists(file_png):
                                pass
                        else:
                            warning_message = u'The images "{0}" does not exist!'.\
                                                format(customer_info_panel_file.file_area_name)
                except Exception, e:
                    print 'Popen Exception =============================== ', e

                # get the lat/lon values for a GeoTIFF files
                try:
                    ds = gdal.Open(file_tif)
                    width = ds.RasterXSize
                    height = ds.RasterYSize
                    gt = ds.GetGeoTransform()
                    minx = gt[0]
                    miny = gt[3] + width*gt[4] + height*gt[5]
                    maxx = gt[0] + width*gt[1] + height*gt[2]
                    maxy = gt[3]
                    centery = (maxy + miny) / 2
                    centerx = (maxx + minx) / 2

                    cLng = centerx
                    cLat = centery
                    eLat_1 = miny
                    eLng_1 = minx
                    eLat_2 = maxy
                    eLng_2 = maxx
                    google_map_zoom = GOOGLE_MAP_ZOOM
                except AttributeError, e:
                    print 'GDAL AttributeError =============================== ', e
        except CustomerInfoPanel.DoesNotExist, e:
            print 'CustomerInfoPanel.DoesNotExist =============================== ', e
            warning_message = u'The file "{0}" does not exist. Perhaps the data is outdated. Please refresh the page and try again.'.format(show_file)
            # return HttpResponseRedirect(
            #     u'%s?danger_message=%s' % (reverse('customer_section'),
            #     (u'The file "{0}" does not exist. Perhaps the data is outdated. Please refresh the page and try again.'.format(show_file)))
            # )

    customer_info_panel_show = CustomerInfoPanel.objects.filter(
                                user=customer,
                                is_show=True)
                                
    try:
        cip_active = CustomerInfoPanel.objects.filter(
                            user=customer,
                            # data_set=data_set,
                            is_show=True)
        # file_tif_path = show_file + '.tif'
        if cip_active:
            file_tif_path = cip_active[0].tif_path
        
        # attribute, units = getAttributeUnits(request.user, show_file)
    except Exception:
        pass
    
    if customer_info_panel_show:
        show_dataset_cip = customer_info_panel_show[0].data_set.name
        show_image_cip = customer_info_panel_show[0].attribute_name
        show_statistic_cip = customer_info_panel_show[0].statisctic
    
        # print 'show_dataset_cip ===================================== ', show_dataset_cip
        # print 'show_image_cip ===================================== ', show_image_cip
        # print 'show_statistic_cip ===================================== ', show_statistic_cip
        
    attribute_report = AttributesReport.objects.filter(user=customer)
    
    if attribute_report:
        for ar in attribute_report:
            show_report_ap.append(ar.shelfdata.attribute_name)
        
    data = {
        'data_sets': data_sets,
        'data_set_id': data_set_id,
        'dirs_list': dirs_list,
        'polygons': polygons,
        'attribute_list_infopanel': attribute_list_infopanel,
        'statisctics_infopanel': statisctics_infopanel,
        'show_dataset_cip': show_dataset_cip,
        'show_image_cip': show_image_cip,
        'show_statistic_cip': show_statistic_cip,
        'show_report_ap': show_report_ap,
        'tab_active': tab_active,
        
        'file_tif_path': file_tif_path,
        
        'warning_message': warning_message,
        
        'absolute_kml_url': absolute_kml_url,
        
        'cLng': cLng,
        'cLat': cLat,
        'eLat_1': eLat_1,
        'eLng_1': eLng_1,
        'eLat_2': eLat_2,
        'eLng_2': eLng_2,
        'GOOGLE_MAP_ZOOM': GOOGLE_MAP_ZOOM,
        'absolute_url_png_file': url_png,
    }

    return data


# PHP calculations
# @user_passes_test(lambda u: u.is_superuser)
@login_required
@render_to('customers/customer_section_php.html')
def customer_section_php(request):
    title = 'PHP page'
    file_tif_path = ''
    coord_list = []
    latlist = ''
    lonlist = ''
    files_tif = ''
    sh_data = ''
    customer = request.user
    customer_tmp_file = str(customer) + '_result.csv'
    customer_tmp_for_db = str(customer) + '_db.csv'
    php_file = '{0}_php_tmp.txt'.format(customer)
    file_path_php = os.path.join(KML_PATH, php_file)
    tmp_file_path = os.path.join(TMP_PATH, customer_tmp_file)
    tmp_db_file_path = os.path.join(TMP_PATH, customer_tmp_for_db)
    result_f_name = 'src/media/temp_files/{0}_result.csv'.format(customer)
    result_for_db = 'src/media/temp_files/{0}_db.csv'.format(customer)
    
    ####################### write log file
    log_file = '/home/gsi/LOGS/delete_file.log'
    log_delete_file = open(log_file, 'w+')
    log_delete_file.write('FILE NAME: '+result_f_name+'\n')
    #######################
    
    # print 'tmp_file_path ============================== ', tmp_file_path
    
    # $latlist = '48.88672158743591,48.86956150482169,48.84019508397442';
    # $lonlist = '-89.83619749546051,-89.57595884799957,-89.75036680698395';
    
    # Handling GET request
    if request.method == "GET":
        data_get_ajax = request.GET
        
        if data_get_ajax.get('tif_path'):
            file_tif_path = data_get_ajax.get('tif_path')
            
            data_set_id = data_get_ajax.get('ds')
            data_set = DataSet.objects.get(id=data_set_id)
            shelf_data = ShelfData.objects.all().order_by('attribute_name')
            
            attributes_reports = AttributesReport.objects.filter(
                                    user=customer, data_set=data_set
                                ).order_by('shelfdata__attribute_name')
                                
            
            
            # dirs_list = getResultDirectory(data_set, shelf_data)
            
            # cip_query = CustomerInfoPanel.objects.filter(
            #                 user=request.user,
            #                 data_set=data_set)
            
            for attr in attributes_reports:
                name_1 = attr.shelfdata.root_filename
                name_2 = data_set.results_directory.split('/')[0]
                tiff_path = os.path.join(PROJECTS_PATH, data_set.results_directory, name_1)
                # files_tif += tiff_path + attr.statisctic + '/mean_ConditionalMean_' + name_1 + '.' + name_2 + '.tif,'
                files_tif += '{0}/{1}_{2}.{3}.tif,'.format(tiff_path, attr.statisctic, name_1, name_2)
                sh_data += '{0},'.format(attr.shelfdata.id)
            
            files_tif = files_tif[0:-1]
            sh_data = sh_data[0:-1]
            
            # print 'dirs_list ============================= ', dirs_list
            # print 'sh_data ============================= ', sh_data
            # print 'files_tif ============================= ', files_tif
            # print 'tmp_db_file_path ============================= ', tmp_db_file_path
            
            try:
                os.remove(tmp_file_path)
                os.remove(tmp_db_file_path)
                
                # print 'remove FILE: "{0}"'.format(tmp_file_path)
                # print 'remove FILE: "{0}"'.format(tmp_db_file_path)
                
                ####################### write log file
                log_delete_file.write('remove FILE: "{0}"\n'.format(tmp_file_path))
                log_delete_file.write('remove DB FILE: "{0}"\n'.format(tmp_db_file_path))
                ####################### write log file
            except Exception, e:
                print 'except REMOVE FILE =========================== ', e
                ####################### write log file
                log_delete_file.write('ERROR remove FILE: "{0}"'.format(e))
                ####################### write log file
                pass
            
            
            f_php_coord = open(file_path_php)
            for line in f_php_coord.readlines():
                coord_list.append(line.replace('\n',''))
                
            # print 'coord_list ============================= ', coord_list
            
            latlist = coord_list[0]
            lonlist = coord_list[1]
            
            # print 'latlist =========================== ', latlist
            # print 'lonlist =========================== ', lonlist
    
    ####################### END write log file
    log_delete_file.close()
    #######################
    
    
    # print 'file_tif_path =========================== ', file_tif_path
    # print 'files_tif =========================== ', files_tif
    
            
    data = {
        'title': title,
        'file_tif_path': file_tif_path,
        'files_tif': files_tif,
        'shelf_data': sh_data,
        'latlist': latlist,
        'lonlist': lonlist,
        'result_f_name': result_f_name,
        'result_for_db': result_for_db,
    }

    return data
    
    
# Delete TMP file
# @user_passes_test(lambda u: u.is_superuser)
@login_required
@render_to('customers/customer_delete_file.html')
def customer_delete_file(request):
    title = ''
    customer = request.user
    result_f_name = str(customer) + '_result.csv'
    result_for_db = str(customer) + '_db.csv'
    result_ajax_file = str(customer) + '_ajax.csv'
    
    tmp_file_path = os.path.join(TMP_PATH, result_f_name)
    db_file_path = os.path.join(TMP_PATH, result_for_db)
    ajax_file_path = os.path.join(TMP_PATH, result_ajax_file)
    
    ####################### write log file
    log_file = '/home/gsi/LOGS/customer_delete_file.log'
    customer_delete_f = open(log_file, 'w+')
    customer_delete_f.write('DB FILE: "{0}"'.format(os.path.exists(db_file_path)))
    #######################
    
    if request.is_ajax() and request.method == "GET":
        data = ''
        data_get_ajax = request.GET
        
        # print 'DELETES FILE data_get_ajax AJAX ============================= ', data_get_ajax
        
        if data_get_ajax.get('delete_file'):
            # time.sleep(5)
            customer_ajax_file = open(ajax_file_path, 'w+')
            data_set_id = data_get_ajax.get('delete_file')
            data_set = DataSet.objects.get(id=data_set_id)
            shelf_data = ShelfData.objects.all()
            data_ajax = ''
            data_ajax_total = ''
            
            while not os.path.exists(db_file_path) and not os.path.exists(tmp_file_path):
                # print 'WHILE DELETE FILES ========================================= '
                time.sleep(10)
                # print 'FILE {0}: {1} ==================================='.format(db_file_path, os.path.exists(db_file_path))
                # print 'FILE {0}: {1} ==================================='.format(tmp_file_path, os.path.exists(tmp_file_path))
                ####################### write log file
                customer_delete_f.write('********************** NO tmp db FILE === \n')
                ####################### write log file
                # pass
            
            print '****************** EXISTS db_file_path ========================================= ', os.path.exists(db_file_path)
            print '****************** EXISTS tmp_file_path ========================================= ', os.path.exists(tmp_file_path)
            
            f_db = open(db_file_path)
            
            for l in f_db:
                line = l.split(',')
                
                print '******************** LINE ========================================= ', line
                
                shd_id = line[0]
                shelf_data = ShelfData.objects.get(id=shd_id)
                data_ajax_total = '{0}_'.format(line[2])
                
                if shelf_data.show_totals:
                    # ha = line[4].replace('\n', ' ha')
                    # ha = '{0}\n'.format(ha)
                    data_ajax += '{0},{1},{2},{3}'.\
                                format(shelf_data.attribute_name, line[3], shelf_data.units, line[4])
                else:
                    data_ajax += '{0},{1},{2}, - \n'.\
                                format(shelf_data.attribute_name, line[3], shelf_data.units)
                
                ####################### write log file
                customer_delete_f.write('data_ajax: "{0}"\n'.format(data_ajax))
                ####################### write log file
                
            data_ajax = data_ajax.replace('\n', '_')
            data_ajax_total += data_ajax[0:-1]
            customer_ajax_file.write(data_ajax_total)
            # customer_ajax_file.write(data_ajax[0:-1])
            f_db.close()
            customer_ajax_file.close()
            
            # print 'data_ajax ====================================== ', data_ajax
            
            ####################### write log file
            customer_delete_f.write('DATA AJAX END: "{0}"\n'.format(data_ajax))
            ####################### write log file
                
            delete_file = '/media/temp_files/' + result_ajax_file
            
            cips = CustomerInfoPanel.objects.filter(user=customer)
            select_static = cips[0].statisctic
            # data = data_ajax
            # file_for_db =
            
            # print 'DATA data_ajax_total ======================= ', data_ajax_total
            # print 'DATA delete_file ======================= ', delete_file
            # print 'DATA select_static ======================= ', select_static
            
            # return HttpResponse(data)
            return HttpResponse(json.dumps({'delete_file':delete_file, 'static': select_static}))
        
    data = {
        'title': title,
    }
    
    ####################### END write log file
    customer_delete_f.close()
    #######################

    return data
