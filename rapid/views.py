from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.core import serializers
#import datetime
from django.utils import timezone
from django.shortcuts import redirect

from django.db.models import Avg, Sum

import csv
#from django.template import RequestContext
# See more http://www.pydanny.com/core-concepts-django-forms.html

from rapid.models import Inventory, Session, TaxonSet, Group, Family, Genus, Species, FolderType
from rapid.forms import InventoryForm, SessionForm, TaxonSetForm


class IndexView(generic.ListView):
    template_name = 'rapid/index.html'
    context_object_name = 'inventory_list'

    def get_queryset(self):
        """Return the inventories."""
        return Inventory.objects.all()

class AboutView(generic.TemplateView):
    template_name = 'rapid/about.html'

class InventoryDetail(generic.DetailView):
    model = Inventory
    template_name = 'rapid/inventory_detail.html'

    # Extend to retrieve all related sessions for inventory
    # from https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InventoryDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the sessions
        context['session_list'] = self.object.session_set.all().order_by('-startTime')
        aggregateSum = self.object.session_set.aggregate(Sum('taxonset__count'))
        #TODO strip decimal value
        # Below added due to bug for new, empty inventory, type error
        try:
            inventory_specimen_count = int(aggregateSum['taxonset__count__sum'])
        except:
            inventory_specimen_count = None
        context['inventory_specimen_count'] = inventory_specimen_count
        context['inventory_session_count'] = self.object.session_set.count()
        #print context['inventory_specimen_count']['taxonset__count__sum']
        #context['inventory_taxonset_count'] =  self.object.session_set.taxonset_set.count()
        # get inventory pk
        self.request.session['current_inventory'] = context['object'].id
        #print self.request.session.get('current_inventory')
        return context


class InventoryStats(generic.DetailView):
    model = Inventory
    template_name = 'rapid/inventory_stats.html'

    # Extend to retrieve all related sessions for inventory
    # from https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InventoryStats, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the sessions
        context['session_list'] = self.object.session_set.all().order_by('-startTime')
        aggregateSum = self.object.session_set.aggregate(Sum('taxonset__count'))
        #TODO strip decimal value
        context['inventory_specimen_count'] = int(aggregateSum['taxonset__count__sum'])
        context['inventory_session_count'] = self.object.session_set.count()
        #print context['inventory_specimen_count']['taxonset__count__sum']
        #context['inventory_taxonset_count'] =  self.object.session_set.taxonset_set.count()
        # get inventory pk
        self.request.session['current_inventory'] = context['object'].id
        #print self.request.session.get('current_inventory')
        return context


def InventoryStatsCSV(request, pk=None):
    #current_inventory = request.session.get('current_inventory')
    current_inventory = Inventory.objects.get(pk=pk)
    #Family.objects.filter(group=group_id)
    sessions = current_inventory.session_set.all().order_by('-startTime')
    print sessions
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="brisc_statistics.csv"'

    writer = csv.writer(response)
    writer.writerow(['session', 'recorder', 'counter', 'start', 'duration(min)', 'sets', 'sets/min', 'specimens', 'specimens/min'])
    for session in sessions:
        writer.writerow([session.id,
            session.recorder,
            session.counter,
            session.startTime,
            session.durationMinutes(),
            session.getCount(),
            session.setsPerMin(),
            session.getSpecimensCounted(),
            session.specimensPerMin()])
    #writer.writerow(['session', 'team', 'start', 'duration', 'sets', 'sets/min', 'specimens', 'specimens/min'])

    return response


class SessionDetail(generic.DetailView):
    model = Session
    template_name = 'rapid/session_detail.html'

    # Extend to retrieve all related taxon sets for session
    # from https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SessionDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the sessions
        context['taxonSet_list'] = self.object.taxonset_set.all()
        #countSum = self.object.taxonset_set.all().aggregate(Sum('count'))
        #print countSum
        # get session pk
        self.request.session['current_session'] = context['object'].id
        #self.request.session['current_session_instance'] = self
        print 'Session details view:', self.request.session.get('current_session')
        return context


class TaxonSetDetail(generic.DetailView):
    model = TaxonSet
    template_name = 'rapid/taxon_set_detail.html'


def new_inventory(request):
# based on https://docs.djangoproject.com/en/1.7/topics/forms/#building-a-form-in-django
# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InventoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_inventory_obj = form.save()
            return HttpResponseRedirect('/inventory/')  # TODO show new inventory detail

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InventoryForm()

    return render(request, 'rapid/inventory_new.html', {'form': form})


def new_session(request):
    current_inventory = request.session['current_inventory']
    if request.method == 'POST':
        recorder = request.POST.get('recorder', None)
        counter = request.POST.get('counter', None)
        new_session_obj = Session(inventory_id=current_inventory, recorder=recorder, counter=counter)
        new_session_obj.save()
        return redirect('session_detail', pk=new_session_obj.id)
        #return redirect('index')
    return render(request, 'rapid/session_new.html')


def new_sessionOLD(request):
# based on https://docs.djangoproject.com/en/1.7/topics/forms/#building-a-form-in-django
# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SessionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_session_obj = form.save()
            #print vars(new_session_obj)
            return redirect('session_detail', pk=new_session_obj.id)
            #return HttpResponseRedirect('/inventory/') #TODO - show new session detail

            # if a GET (or any other method) we'll create a blank form
    else:
        form = SessionForm()

    return render(request, 'rapid/session_new.html', {'form': form})


def end_session(request):
    current_session = request.session.get('current_session')
    current_inventory = request.session.get('current_inventory')
    #print current_session
    #print vars(new_session_obj)
    now = timezone.now()
    current_session_obj = Session.objects.get(id=current_session)
    current_session_obj.endTime = now
    current_session_obj.save()
    # TODO - set msq here
    #msg = 'Session #' + str(current_session) + ' completed at ' + str(now)
    # Try to put msg in session then display in destination page
    # see http://stackoverflow.com/questions/9488874/django-redirect-with-parameters
    return redirect('inventory_detail', current_inventory)


    #return render('inventory_detail', current_inventory, {'msg': msg})
    #return render(request, 'rapid/session_new.html', {'form': form})

    # Not using this now
def new_taxon_set(request):
# based on https://docs.djangoproject.com/en/1.7/topics/forms/#building-a-form-in-django
# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaxonSetForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            # https://docs.djangoproject.com/en/1.7/topics/forms/modelforms/#the-save-method
            new_taxon_set_obj = form.save(commit=False)
            #current_session_instance = Session.objects.get(pk=1)
            #TODO - how to do this without retrieving session obj?
            current_session_instance = Session.objects.get(pk=request.session['current_session'])
            new_taxon_set_obj.session = current_session_instance
            # current_group_id =
            request.session['current_group_id'] = context['object'].id
            # self.request.session['current_session'] = context['object'].id
            #new_taxon_set_obj.session_ID = '1' # must be a Session instance, not a number
            # http://stackoverflow.com/questions/22739701/django-save-modelform
            new_taxon_set_obj.save()
            #http://stackoverflow.com/questions/15852841/django-prepopulate-modelform-nothing-happens

            data['count'] = '1'  # set initial value to 1 for next form
            form = TaxonSetForm(initial=data)
            return render(request, 'rapid/taxon_set_new.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        # This seems to try to create a form with all the taxa objects - essentially querying the DB for all the thousands of taxa and populating the SELECT lists.
        form = TaxonSetForm()

    #form.cleaned_data['count'] = None
    return render(request, 'rapid/taxon_set_new.html', {'form': form})


def new_taxon(request):
    #parent_rank=request.GET.get('parent_rank')
    #parent_id=request.GET.get('parent_id')
    #child_name=request.GET.get('child_name')
    parent_rank = request.POST.get('parent_rank')
    parent_id = request.POST.get('parent_id')
    child_name = request.POST.get('child_name')
    #print parent_rank, parent_id, child_name
    #print request
    if parent_rank == 'family':
        #print 'Make genus', child_name , 'with family_id', parent_id
        new_genus = Genus(name=child_name, family_id=parent_id, status='unverified', source='BRIT inventory')
        new_genus.save()
        print 'New genus created:', new_genus.name, new_genus.pk, 'for family:', parent_id
        return HttpResponse("Genus created")

    if parent_rank == 'genus':
        #print 'Make species', child_name , 'with genus_id', parent_id
        new_species = Species(name=child_name, genus_id=parent_id, status='unverified', source='BRIT inventory')
        new_species.save()
        print 'New species created:', new_species.name, new_species.pk, 'for genus:', parent_id
        return HttpResponse("Species created")
    #return render(request, 'rapid/index.html')
    return HttpResponse("nothing created")


def taxa(request, mode=None, pk=None):
    #TODO - make form settings based on GET request
    #TODO - make TaxonSet record save based on POST
    print mode
    taxaDict = {}
    foldertype_id = 1  # Set default folder
    current_session = request.session.get('current_session')
    current_inventory = request.session.get('current_inventory')
    print 'Taxon Set Count:'
    print 'current_inventory:', current_inventory
    print 'current_session:', current_session

    if request.method == 'GET':
        # starting to try to display existing counts for editing
        print "PK:", pk
        # Initialize values, first view of form
        try:
            group_id
        except:
            group_id = None
        try:
            family_id
        except:
            family_id = None
        try:
            genus_id
        except:
            genus_id = None
        try:
            species_id
        except:
            species_id = None
        try:
            container
        except:
            container = None
        try:
            msg
        except:
            msg = ''
        try:
            note
        except:
            note = ''

        if pk is not None:
            try:
                taxonSetPreviouslyCounted = TaxonSet.objects.get(pk=pk)
                print taxonSetPreviouslyCounted
            except:
                print 'Taxon set does not exist:', pk
            #print count.pk, count.group_id, count.family_id, count.genus_id, count.species_id

            #TODO move this to try section
            group_id = taxonSetPreviouslyCounted.group_id
            family_id = taxonSetPreviouslyCounted.family_id
            genus_id = taxonSetPreviouslyCounted.genus_id
            species_id = taxonSetPreviouslyCounted.species_id
            container = taxonSetPreviouslyCounted.container
            foldertype_id = taxonSetPreviouslyCounted.folder_id
            count = taxonSetPreviouslyCounted.count
            note = taxonSetPreviouslyCounted.note
            session = taxonSetPreviouslyCounted.session
            session_id = session.id
            inventory_id = session.inventory.id
            count_id = pk
            #print session.inventory, inventory_id, session, session_id

    if request.method == 'POST':
        group_id = request.POST.get('group_id', None)
        family_id = request.POST.get('family_id', None)
        genus_id = request.POST.get('genus_id', None)
        species_id = request.POST.get('species_id', None)
        count = request.POST.get('count', None)
        note = request.POST.get('note', None)
        foldertype_id = request.POST.get('foldertype_id', None)
        container = request.POST.get('container', None)

    #TODO - only filter children when parent has an established ID
    foldertypes = FolderType.objects.all()
    #groups = Group.objects.all().order_by('name')
    groups = Group.objects.all().order_by('id')
    families = Family.objects.filter(group=group_id).order_by('name')
    genera = Genus.objects.filter(family=family_id).order_by('name')
    species = Species.objects.filter(genus=genus_id).order_by('name')

    # set up taxaDict to contain selected taxa
    #TODO stop using taxaDict? just put taxon IDs into context?
    taxaDict['group_id'] = group_id
    taxaDict['family_id'] = family_id
    taxaDict['genus_id'] = genus_id
    taxaDict['species_id'] = species_id


    if request.method == 'POST':
        if mode == 'edit':
            taxonSetEdited = TaxonSet.objects.get(pk=pk)
            taxonSetEdited.group_id = group_id
            taxonSetEdited.family_id = family_id
            taxonSetEdited.genus_id = genus_id
            taxonSetEdited.species_id = species_id
            taxonSetEdited.count = count
            taxonSetEdited.container = container
            taxonSetEdited.folder_id = foldertype_id
            taxonSetEdited.note = note
            #endTime = now #Not changing timestamps
            taxonSetEdited.save()
            msg = 'Changes saved: ' + taxonSetEdited.getSummary() + ' - count ID: ' + str(taxonSetEdited.id) + ' Notes: ' + taxonSetEdited.note
            print 'Updated:' + str(taxonSetEdited.id) + ' - ', taxonSetEdited.getSummary()  # + ' Inv:' + current_inventory + ' Sesn:' + current_session
            return redirect('count_detail', pk=pk)

        else:  # create mode
            now = timezone.now()
            taxon_set_obj = TaxonSet(group_id=group_id,
                family_id=family_id,
                genus_id=genus_id,
                species_id=species_id,
                count=count,
                container=container,
                endTime=now,
                session_id=current_session,
                folder_id=foldertype_id,
                note=note,
                )
            taxon_set_obj.save()
            msg = 'Saved: ' + taxon_set_obj.getSummary() + ' - count ID: ' + str(taxon_set_obj.id) + ' Notes: ' + taxon_set_obj.note
            print taxon_set_obj.getSummary()  # + ' Inv:' + current_inventory + ' Sesn:' + current_session

    # for create mode 'session' and 'count_id' isn't initiliazed or used
    try:
        session
    except:
        session = None
    try:
        count_id
    except:
        count_id = None
    try:
        count
    except:
        count = 1

    return render(request, 'rapid/taxa_form.html', {
        'folder_id_selected': foldertype_id,
        'foldertypes': foldertypes,
        #TODO use each taxon id instead of taxaDict?
        'taxaDict': taxaDict,
        'groups': groups,
        'families': families,  # TODO remove from dict?
        'genera': genera,
        'species': species,
        'container': container,
        'current_session': current_session,
        'current_inventory': current_inventory,
        'session': session,  # for edit mode of past counts
        'msg': msg,
        'mode': mode,
        'count_id': count_id,
        'count': count,
        'note': note,
        })


def taxa_in_taxon(request, taxon_rank=None, taxon_id=None):
    print taxon_rank, taxon_id
    if taxon_rank == 'group':
        taxa = Family.objects.filter(group=taxon_id).extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
    elif taxon_rank == 'family':
        taxa = Genus.objects.filter(family=taxon_id).extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
    elif taxon_rank == 'genus':
        taxa = Species.objects.filter(genus=taxon_id).extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
    elif taxon_rank == 'species':
        taxa = None  # species don't contain any taxa in this model
    else:
        taxa = None
    taxa_list = []
    for taxon in taxa:
        #taxa_dict[taxon.pk] = taxon.name
        #TODO determine if item is selected and pass 'TRUE', or maybe this is handled somewhere else?
        taxa_list.append([taxon.pk, taxon.name.encode('utf8', 'ignore'), 'TRUE'])

    # TODO render taxonSet detail page after edit instead of next coutn form
    return render(request, 'rapid/taxa_in_taxon_json.html', {'taxa': taxa, 'taxa_list': taxa_list})
