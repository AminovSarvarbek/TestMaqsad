from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import models
from django import forms
from django.http import Http404

def dynamic_model_list(request, app_label, model_name):
    """
    List all objects of a dynamic model with search and pagination capabilities.
    """
    try:
        # Retrieve the model class using the app label and model name
        model = ContentType.objects.get(app_label=app_label, model=model_name.lower()).model_class()
    except ContentType.DoesNotExist:
        # Handle case where model is not found
        raise Http404

    # Get the search query from GET parameters
    query = request.GET.get('q', '')
    object_list = model.objects.all()

    # Create a Q object for searching across all text fields
    search_queries = Q()
    for field in model._meta.fields:
        # Skip non-text fields such as ForeignKey
        if isinstance(field, (models.CharField, models.TextField)):
            search_queries |= Q(**{f"{field.name}__icontains": query})

    # Filter object list based on search queries
    object_list = model.objects.filter(search_queries)

    # Pagination setup: Show 10 objects per page
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    # Get field names to display in the template
    field_names = [field.name for field in model._meta.fields if not field.name.startswith('_')]

    # Prepare context data for rendering the template
    context = {
        'objects': objects,
        'query': query,
        'model_name': model_name,
        'field_names': field_names,
        'app_label': app_label,
    }
    
    return render(request, 'admin/crud/model_list.html', context)

def dynamic_model_form(request, app_label, model_name, pk=None):
    """
    Handle the creation and updating of dynamic model instances.
    """
    try:
        # Retrieve the model class using the app label and model name
        global model
        model = ContentType.objects.get(app_label=app_label, model=model_name.lower()).model_class()
    except ContentType.DoesNotExist:
        # Handle case where model is not found
        raise Http404

    # Retrieve the object if primary key (pk) is provided; otherwise, create a new one
    obj = get_object_or_404(model, pk=pk) if pk else None

    # Dynamically create a ModelForm for the model
    class DynamicForm(forms.ModelForm):
        class Meta:
            model = model  # Reference the dynamic model
            fields = '__all__'  # Include all fields in the form

    if request.method == 'POST':
        form = DynamicForm(request.POST, instance=obj)  # Bind form to POST data
        if form.is_valid():
            form.save()  # Save the form and redirect
            return redirect('custom_admin:dynamic_model_list', app_label=app_label, model_name=model_name)
    else:
        form = DynamicForm(instance=obj)  # Create form instance for GET request

    # Render the form template with context data
    return render(request, 'admin/crud/model_form.html', {
        'form': form,
        'model_name': model_name,
        'app_label': app_label,  # Pass app_label for context
        'model_name': model_name  # Pass model_name for context
    })

def dynamic_model_delete(request, app_label, model_name, pk):
    """
    Handle the deletion of a dynamic model instance.
    """
    try:
        # Retrieve the model class using the app label and model name
        model = ContentType.objects.get(app_label=app_label, model=model_name.lower()).model_class()
    except ContentType.DoesNotExist:
        # Handle case where model is not found
        raise Http404

    # Retrieve the object to be deleted
    obj = get_object_or_404(model, pk=pk)
    
    if request.method == 'POST':
        obj.delete()  # Delete the object and redirect
        return redirect('custom_admin:dynamic_model_list', app_label=app_label, model_name=model_name)

    # Render the confirmation delete template with context data
    return render(request, 'admin/crud/model_confirm_delete.html', {
        'object': obj,
        'model_name': model_name,
        'app_label': app_label,  # Pass app_label for context
    })
