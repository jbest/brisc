from django.db import models
from django.db.models import Sum
from datetime import timedelta


class FolderType(models.Model):
    """Type of folder containing specimens
    Folder types represent different collections
    and geographic scopes.
    They are designated by name and color.
    """
    name = models.CharField(max_length=50, default='')  # Short name based on color and geo scope
    color = models.CharField(max_length=50)
    geographicScope = models.CharField(max_length=50)
    collection = models.CharField(max_length=50)
    collectionCode = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name + '-' + self.color


class Group(models.Model):
    """Taxonomic group e.g. monocots, dicots, etc.
    Top-level taxonomic rank containing families.

    Attributes:
        name    Name representing the group
        status  
        source  The source of the group name
    """
    name = models.CharField(max_length=200, null=False, default='NONE')
    status = models.CharField(max_length=200, null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):  # __unicode__ on Python 2, __str__ for 3
        return self.name


class Family(models.Model):
    """Taxonomic rank under Group containing Genera

    Attributes:
        group   The group containing this family.
        name    Name representing the family
        status  
        source  The source of the group name
    """
    group = models.ForeignKey(Group, null=True)
    name = models.CharField(max_length=200, null=False, default='NONE')
    status = models.CharField(max_length=200, null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Families"

    def __unicode__(self):  # __unicode__ on Python 2, __str__ for 3
        return self.name


class Genus(models.Model):
    """

    Attributes:
        family  Family taxon containing this genus.
        name    Name representing the genus.
        status  
        source  The source of the genus name.
    """
    family = models.ForeignKey(Family)
    name = models.CharField(max_length=200, null=False, default='NONE')
    status = models.CharField(max_length=200, null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Genera"

    def __unicode__(self):  # __unicode__ on Python 2, __str__ for 3
        return self.name


class Species(models.Model):
    """
    Attributes:
        genus   Genus containing this species.
        name    Name representing the species.
        status  
        source  The source of the species name.
    """
    genus = models.ForeignKey(Genus)
    name = models.CharField(max_length=200, null=False, default='NONE')
    status = models.CharField(max_length=200, null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Species"

    def __unicode__(self):  # __unicode__ on Python 2, __str__ for 3
        return self.name


class Inventory(models.Model):
    """A count of a collection or part of a collection.

    Attributes:
        startDate   The date that the inventory begins.
        endDate     The date that the inventory ends.
        description A short description of the inventory.  
        notes       Notes about the inventory.
    """
    startDate = models.DateTimeField('start date of inventory')
    endDate = models.DateTimeField('end date of inventory')
    description = models.CharField(max_length=200, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "inventories"

    def __unicode__(self):  # __unicode__ on Python 2, __str__ for 3
        #return str(self.startDate)
        return str(self.pk) + ' - ' + self.startDate.strftime('%Y-%m-%d')

    def teamMinutes(self):
        return None


class Session(models.Model):
    inventory = models.ForeignKey(Inventory, null=True)
    startTime = models.DateTimeField('start time of session', null=True, blank=True, auto_now_add=True)
    endTime = models.DateTimeField('end time of session', null=True, blank=True)  # , auto_now=True
    recorder = models.CharField(max_length=200, null=True)
    counter = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):  # __unicode__ on Python 2, __str__ for 3
        #return 'Inv: ' + str(self.inventory) + ' ' + self.recorder
        return 'Inv:' + str(self.inventory_id) + ' S:' + str(self.pk) + ' - ' + self.recorder

    def getSpecimensCounted(self):
        # TODO - use aggregations -https://docs.djangoproject.com/en/1.7/topics/db/aggregation/
        #specimen_count = TaxonSet.objects.filter(session=self).aggregate(Sum('count'))
        #return specimen_count
        # this returns '{'count__sum': 45}'
        sets_in_session = TaxonSet.objects.filter(session=self)
        specimen_count = 0
        for taxon_set in sets_in_session:
            #some entries have None or some character that can't be converted to int
            try:
                count = int(taxon_set.count)
            except:
                count = 0
            #print 'taxon_set.count:', taxon_set.count, type(taxon_set.count)
            #count = 0 if int(taxon_set.count) is None else int(taxon_set.count)
            #print count
            specimen_count += count
        return specimen_count

    def getCount(self):
        session_taxon_sets = TaxonSet.objects.filter(session=self)
        return len(session_taxon_sets)

    #TODO create one property or function that does all stat calculaitons once and returns values
    # Rather than multiple calls which repeatedly use related calculations.
    def durationSeconds(self):
        if self.endTime is not None:
            tdelta = self.endTime - self.startTime
            seconds = tdelta.total_seconds()
            return seconds
        else:
            return None

    def durationMinutes(self):
        try:
            seconds = self.durationSeconds()
            return seconds / 60
        except:
            return None

    def setsPerMin(self):
        if self.endTime is not None:
            duration = self.durationMinutes()
            return str("%0.2f" % (self.getCount() / duration))
        else:
            return None

    def specimensPerMin(self):
        if self.durationMinutes() is not None:
            return str("%0.2f" % (self.getSpecimensCounted() / self.durationMinutes()))
        else:
            return None


class TaxonSet(models.Model):
    """An inventory of a group of specimens within a taxon
    Inventoried in a single container by an inventory team during a session.
    """
    session = models.ForeignKey(Session, null=True)
    folder = models.ForeignKey(FolderType, null=True)
    container = models.CharField(max_length=50, null=True)
    note = models.CharField(max_length=200, null=True, blank=True)
    #startTime = models.DateTimeField('start time of session', null=True, blank=True, auto_now_add=True) #TODO
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField('end time of taxon set - when submitted', null=True, blank=True)
    group = models.ForeignKey(Group, null=True) or None
    family = models.ForeignKey(Family, null=True) or None
    genus = models.ForeignKey(Genus, null=True) or None
    species = models.ForeignKey(Species, null=True) or None
    #TODO validate count as a number?
    #Or use IntegerField? https://docs.djangoproject.com/en/1.7/ref/models/fields/#integerfield
    count = models.CharField(max_length=3, null=False, default='0')

    def __unicode__(self):  # __unicode__ on Python 2, __str__ for 3
        return str(self.id) + '-' + str(self.session) + ' ' + str(self.genus) + ' ' + str(self.species)

    def getSummary(self):
        summary = ''
        summary += str(self.family.name) + ' ' if self.family else ' none '
        summary += str(self.genus.name) + ' ' if self.genus else ' none '
        summary += str(self.species.name) + ' ' if self.species else ' none '
        summary += str(self.count) + ' ' if self.count else ' none'
        return summary
        #return str(self.family.name) + ' ' + str(self.genus.name) + ' ' + str(self.species.name) + ':' + str(self.count)
