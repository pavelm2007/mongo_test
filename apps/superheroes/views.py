# Create your views here.
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import *
from forms import *
from gridfs import GridFS, NoFile
from mongoengine.connection import get_db
from bson.objectid import ObjectId
from django.http import Http404, HttpResponse
from django.utils.http import http_date

from .forms import PowerFilterForm

def serve_file(request, file_id):
    db = get_db()
    fs = GridFS(db)
    try:
        f = fs.get(ObjectId(file_id))
    except NoFile:
        fs = GridFS(db, collection='images') # mongoengine stores images in a separate collection by default
        try:
            f = fs.get(ObjectId(file_id))
        except NoFile:
            raise Http404

    response = HttpResponse(f.read(), content_type=f.content_type)
    # timestamp = time.mktime(gridout.upload_date.timetuple())
    # response["Last-Modified"] = http_date(timestamp)
    # add other header data like etags etc. here
    return response

class AlteregosListView(ListView):
    model = Alteregos
    context_object_name = "hero_list"

    def get_template_names(self):
        return ["superheroes/list.html"]

    def get_queryset(self):

        filters = self.request.GET.get('filter', None)
        if filters != 'all' and not filters is None:
            power = Power.objects(id=filters)[0]
            return Alteregos.objects(is_published=True, powers_obj_list__in=[power])

        if 'all_heroes' not in self.request.GET:
            return Alteregos.objects(is_published=True)
        return Alteregos.objects

    def get_context_data(self, **kwargs):
        ctx = super(AlteregosListView, self).get_context_data(**kwargs)
        form = PowerFilterForm(self.request.GET or None)
        ctx['form'] = form
        return ctx


class AlteregosCreateView(CreateView):
    model = Alteregos
    form_class = AlteregosForm

    def get_template_names(self):
        return ["superheroes/create.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        messages.success(self.request, "The hero has been created.")
        return super(AlteregosCreateView, self).form_valid(form)


class AlteregosDetailView(DetailView):
    model = Alteregos
    context_object_name = "hero"

    def get_template_names(self):
        return ["superheroes/detail.html"]

    def get_object(self):
        return Alteregos.objects(id=self.kwargs['pk'])[0]


class AlteregosUpdateView(UpdateView):
    model = Alteregos
    form_class = AlteregosForm
    context_object_name = "post"

    def get_template_names(self):
        return ["superheroes/update.html"]

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        self.object = form.save()
        formset = self.get_formset(request=True)
        if formset.is_valid():
            for form_item in formset:
                image_item = form_item.save()
                self.object.images.append(image_item.to_dbref())
        # self.object = form.save(commit=False)
        messages.success(self.request, "The hero has been updated.")

        return super(AlteregosUpdateView, self).form_valid(form)

    def get_object(self):
        return Alteregos.objects(id=self.kwargs['pk'])[0]

    def get_formset(self, **kwargs):
        request = kwargs.get('request', None)
        formset = formset_factory(ImageForm)
        if request:
            formset = formset(self.request.POST, self.request.FILES)
        return formset

    def get_context_data(self, **kwargs):
        ctx = super(AlteregosUpdateView, self).get_context_data(**kwargs)
        ctx.update(
            {
                'formset_image': self.get_formset()
            }
        )
        return ctx


class AlteregosDeleteView(DeleteView):
    model = Alteregos

    def get_success_url(self):
        return reverse('list')

    def get(self, *args, **kwargs):
        """ Skip confirmation page """
        return self.delete(self.request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "The hero has been removed.")
        return redirect(self.get_success_url())

    def get_object(self):
        return Alteregos.objects(id=self.kwargs['pk'])[0]


class PowerCreateView(CreateView):
    model = Power
    form_class = PowerForm
    template_name = 'superheroes/create.html'

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        messages.success(self.request, "The power has been created.")
        return super(PowerCreateView, self).form_valid(form)


