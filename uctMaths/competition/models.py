# models.py
# defines django models (correspond to db tables)

from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class School(models.Model):
    # Contains school information. Duplicates should not be allowed, but will be removed by the admin.
    name        = models.CharField(max_length=40L, db_column='Name') 
    key         = models.CharField(max_length=3L, db_column='Key') 
    language    = models.CharField(max_length=1L, choices=(
        ('e', 'English'), 
        ('a', 'Afrikaans')
    ), db_column = 'Language')
    address     = models.CharField(max_length=50L, db_column='Address', blank=True) 
    phone       = models.CharField(max_length=15L, db_column='Phone', blank=True) 
    fax         = models.CharField(max_length=15L, db_column='Fax', blank=True) 
    contact     = models.CharField(max_length=30L, db_column='Contact', blank=True) 
    entered     = models.IntegerField(null=True, db_column='Entered', blank=True) 
    score       = models.IntegerField(null=True, db_column='Score', blank=True) 
    email       = models.CharField(max_length=30L, db_column='Email', blank=True)
    registered_by = models.ForeignKey(User, db_column='Registered By')
 
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']     #defines the way the records are sorted.

class SchoolStudent(models.Model):
    # A single student. Not a User. Score and Rank will added/updated by the admin so they can be null.
    firstname   = models.CharField(max_length=32L, db_column='First_name') 
    surname     = models.CharField(max_length=32L, db_column='Surname')
    language    = models.CharField(max_length=1L, choices=(
        ('e', 'English'), 
        ('a', 'Afrikaans')
    ), db_column = 'Language')
    reference   = models.CharField(max_length=7L, db_column='Reference') 
    school      = models.ForeignKey('School', db_column='School') 
    score       = models.IntegerField(null=True, db_column='Score', blank=True) 
    rank        = models.IntegerField(null=True, db_column='Rank', blank=True) 
    grade       = models.IntegerField(db_column='Grade', 
        validators = [
            MaxValueValidator(12),
            MinValueValidator(0)
        ])    
    sex         = models.CharField(max_length=1L, db_column='Sex', blank=True) 
    venue       = models.CharField(max_length=40L, db_column='Venue', blank=True) 
    registered_by = models.ForeignKey(User, db_column='Registered By')
    def __str__(self):
        return 'pair '+str(self.reference) if self.surname == '' else self.surname+', '+self.firstname
    class Meta:
        ordering = ['grade', 'surname', 'firstname','reference'] #defines the way the records are sorted.

class SchoolUser(models.Model):
    # The administrator for a single school. 
    # A User can register/update/remove SchoolStudents and Invigilators.

    school      = models.ForeignKey('School', db_column='School') 
    count       = models.IntegerField()
    address     = models.CharField(max_length=40L, db_column='Address') 
    town        = models.CharField(max_length=20L, db_column='Town') 
    postal_code = models.CharField(max_length=4L, db_column='Postal_Code') 
    phone       = models.CharField(max_length=15L, db_column='Telephone') 
    fax         = models.CharField(max_length=15L, db_column='Fax', blank=True) 
    email       = models.CharField(max_length=40L, db_column='Email', blank=True) 
    correction  = models.IntegerField(db_column='Correction') 
    entered     = models.IntegerField(db_column='Entered')  
    language    = models.CharField(max_length=1L, db_column='Language', choices=(
        ('e', 'English'), 
        ('a', 'Afrikaans')
    )) 
    counter     = models.IntegerField(db_column='Count')
    last_login  = models.DateField(null=True, blank=True, db_column='Last Login')
    non_uct     = models.IntegerField(db_column='Non UCT') 
    user        = models.OneToOneField(User)

    def __str__(self):
        return self.user
    class Meta:
        ordering = ['school', 'user'] #defines the way the records are sorted.

class Venue(models.Model):
    '''Venues are locations for the event. Many SchoolStudents to one Venue.'''
    code        = models.CharField(max_length=40L, db_column='Code')
    building    = models.CharField(max_length=40L, db_column='Building') 
    seats       = models.IntegerField(db_column='Seats')
    bums        = models.IntegerField(db_column='Bums')
    grade       = models.IntegerField(db_column='Grade')
    pairs       = models.IntegerField(db_column='Pairs')
    registered_by = models.ForeignKey(User, db_column='Registered By')

    def __str__(self):
        return self.building+', '+self.code
    class Meta:
        ordering = ['building', 'code'] #defines the way the records are sorted.

class Invigilator(models.Model):
    # Invigilators registered by SchoolUsers. Many Invigilator to one School. 
    # Many Invigilators to one Venue.

    school      = models.ForeignKey('School', db_column='School') 
    firstname   = models.CharField(max_length=32L, db_column='First_name') 
    surname     = models.CharField(max_length=32L, db_column='Surname')
    grade       = models.IntegerField(db_column='Grade', null=True,
        validators = [
            MaxValueValidator(12),
            MinValueValidator(0)
        ])
    venue       = models.ForeignKey('Venue', db_column='Venue', null=True, blank=True) 
    inv_reg     = models.CharField(max_length=1L, choices=(
        ('i', 'Invigilator'), 
        ('r', 'Registrator')
    ), db_column='Inv_Reg')
    phone_h     = models.CharField(max_length=15L, db_column='Phone (H)', blank=True) 
    phone_w     = models.CharField(max_length=15L, db_column='Phone (W)', blank=True) 
    fax_h       = models.CharField(max_length=15L, db_column='Fax (H)', blank=True) 
    fax_w       = models.CharField(max_length=15L, db_column='Fax (W)', blank=True) 
    email       = models.CharField(max_length=40L, db_column='Email', blank=True) 
    responsible = models.CharField(max_length=40L, db_column='Responsible')
    registered_by = models.ForeignKey(User, db_column='Registered By')
    def __str__(self):
        return self.surname+', '+self.firstname
    class Meta:
        ordering = ['school', 'surname', 'firstname'] #defines the way the records are sorted.
        

class SchoolStudentArchive(models.Model):
    # Duplicate of the SchoolStudent model with extra date field - 'archived'. Used for saving old data. 
    # Generated from the admin page 
    
    archived    = models.DateField(null=True, blank=True, db_column='Date Archived')
    firstname   = models.CharField(max_length=32L, db_column='First_name') 
    surname     = models.CharField(max_length=32L, db_column='Surname')
    language    = models.CharField(max_length=1L, choices=(
        ('e', 'English'), 
        ('a', 'Afrikaans')
    ), db_column = 'Language')
    reference   = models.CharField(max_length=7L, db_column='Reference') 
    school      = models.ForeignKey('School', db_column='School') 
    score       = models.IntegerField(null=True, db_column='Score', blank=True) 
    rank        = models.IntegerField(null=True, db_column='Rank', blank=True) 
    grade       = models.IntegerField(db_column='Grade', 
        validators = [
            MaxValueValidator(12),
            MinValueValidator(0)
        ])    
    sex         = models.CharField(max_length=1L, db_column='Sex', blank=True) 
    venue       = models.CharField(max_length=40L, db_column='Venue', blank=True) 
    registered_by = models.ForeignKey(User, db_column='Registered By')
    def __str__(self):
        return 'pair '+str(self.reference) if self.surname == '' else self.surname+', '+self.firstname+' ('+self.archived+')'
    class Meta:
        ordering = ['archived','grade', 'surname', 'firstname','reference'] #defines the way the records are sorted.



class InvigilatorArchive(models.Model):
    # duplicate of the Invigilator model with extra date field - 'archived'. Used for saving old data. 
    # Generated from the admin page     

    archived    = models.DateField(null=True, blank=True, db_column='Date_Archived')
    school      = models.ForeignKey('School', db_column='School') 
    firstname   = models.CharField(max_length=32L, db_column='First_name') 
    surname     = models.CharField(max_length=32L, db_column='Surname')
    grade       = models.IntegerField(db_column='Grade', null=True,
        validators = [
            MaxValueValidator(12),
            MinValueValidator(0)
        ])
    venue       = models.ForeignKey('Venue', db_column='Venue', null=True, blank=True) 
    inv_reg     = models.CharField(max_length=1L, choices=(
        ('i', 'Invigilator'), 
        ('r', 'Registrator')
    ), db_column='Inv_Reg')
    phone_h     = models.CharField(max_length=15L, db_column='Phone (H)', blank=True) 
    phone_w     = models.CharField(max_length=15L, db_column='Phone (W)', blank=True) 
    fax_h       = models.CharField(max_length=15L, db_column='Fax (H)', blank=True) 
    fax_w       = models.CharField(max_length=15L, db_column='Fax (W)', blank=True) 
    email       = models.CharField(max_length=40L, db_column='Email', blank=True) 
    responsible = models.CharField(max_length=40L, db_column='Responsible')
    registered_by = models.ForeignKey(User, db_column='Registered By')
    def __str__(self):
        return self.surname+', '+self.firstname+' ('+str(self.archived)+')'
    class Meta:
        ordering = ['archived', 'school', 'surname', 'firstname'] #defines the way the records are sorted.