# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import loader, Context
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django import forms
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from competition.forms import StudentForm, SchoolForm, InvigilatorForm
from competition.models import SchoolStudent, School, Invigilator, Venue 
from django.contrib.auth.models import User
from django.db import connection
from django.contrib.auth.decorators import login_required


# def auth(request):
#   if not request.user.is_authenticated():
#     print "not logged in"
#     return HttpResponseRedirect('/accounts/login')

def index(request):
	return render_to_response('index.html', {})


@login_required
def profile(request):
  # auth(request)
  return render_to_response('profile.html',{})


# submitted thingszz
@login_required
def submitted(request, c):
  return render_to_response('submitted.html', c)

#********************************************
# View Students
#Can view a list of students registered by current user 
#User can also delete the entire list or can edit individual students
@login_required
def students(request):
    username = request.user #Current user
    studentOptions = SchoolStudent.objects.filter(registered_by = username) #Gets all the students who were registered by current user
    
    #If the user decides to delete the list. Delete only students registered by the current user
    if request.method=='POST' and 'delete' in request.POST:
        form = (request.POST) # A form bound to the POST data
        for i in range (studentOptions.count()): 
          studentUpdate = SchoolStudent.objects.get(id = form.getlist('studentID','')[i])
          studentUpdate.delete()
    
    #If the user edits teh students. Edits can only be made to certain fields     
    elif request.method=='POST' and 'submit' in request.POST:
        form = (request.POST) # A form bound to the POST data
        for i in range (studentOptions.count()):
          studentID = form.getlist('studentID','')[i]
          studentUpdate = SchoolStudent.objects.get(id = studentID)
          studentUpdate.firstname = form.getlist('firstname','')[i]
          studentUpdate.surname = form.getlist('surname','')[i]
          studentUpdate.sex = form.getlist('sex','')[i]
          studentUpdate.save()
         
    c = {'students':studentOptions} #Passes the list of students for the current user
    c.update(csrf(request))
    return render_to_response('students.html', c,context_instance=RequestContext(request))

#*******************************************
# View Schools
#View the list of schools registered by current user
#Can either delete the whole list or edit individual schools
@login_required
def schools(request):
    username = request.user #current user
    schoolOptions = School.objects.filter(registered_by = username)
    
    #If the user decides to delete all the schools. Deletes only schools registered by that user
    if request.method=='POST' and 'delete' in request.POST:
        form = (request.POST) # A form bound to the POST data
        for i in range (schoolOptions.count()): #RANGE!!!!!!!!
          schoolID = form.getlist ('schoolID',"")[i]
          
          #SQL to DELETE schools
          cursor = connection.cursor()
          cursor.execute("DELETE FROM competition_school WHERE id=%s", [schoolID])
          row = cursor.fetchone()

          #Code below didnt work, for some unknown reason, therefore we used the above SQL to DELETE
          # print "id ", schoolID
          # temp = School.objects.get(id = schoolID)
          # print temp
          # temp.delete()
          # School.objects.get(id = schoolID).delete()
          #   print 'iteration:',i,School.objects.get(id=i+1), type(form.getlist('schoolID','')[0])
          #   schoolID = form.getlist('schoolID','')[i]
          #   schoolUpdate = School.objects.get(id = schoolID)
          #   schoolUpdate.delete()

    #If the user decides to edit schools. Edits can only be made to certain fields
    elif request.method=='POST' and 'submit' in request.POST:
        form = (request.POST) # A form bound to the POST data
        for i in range (schoolOptions.count()):
          schoolID = form.getlist('schoolID','')[i]
          schoolUpdate = School.objects.get(id = schoolID)
          schoolUpdate.name = form.getlist('name','')[i]
          schoolUpdate.address = form.getlist('address','')[i]
          schoolUpdate.language = form.getlist('language','')[i]
          schoolUpdate.phone = form.getlist('phone','')[i]
          schoolUpdate.email = form.getlist('email','')[i]
          schoolUpdate.contact = form.getlist('contact','')[i]
          schoolUpdate.fax = form.getlist('fax','')[i]
          schoolUpdate.save()
          
    c = {'schools':schoolOptions} #Sends back list of schools registered by that person
    c.update(csrf(request))
    return render_to_response('schools.html', c, context_instance=RequestContext(request))

#***************************************************
# View Invigilators
#Can view a list of invigilators which the current user has registered
#Current user can also delete the list or edit the invigilators
@login_required
def invigilators(request):
    username = request.user #current user
    invigilators = Invigilator.objects.filter(registered_by = username)
    
    #If the user decides to delete the list. Only deletes invigilators registered by the current user
    if request.method=='POST' and 'delete' in request.POST:
        form = (request.POST) # A form bound to the POST data
        for i in range (invigilators.count()):
          invigilatorUpdate = Invigilator.objects.get(id = form.getlist('invigilatorID','')[i])
          invigilatorUpdate.delete()

    #If the user decides to edit the invigilators' information
    elif request.method=='POST' and 'submit' in request.POST:
        form = (request.POST) # A form bound to the POST data
        for i in range (invigilators.count()): #RANGE!!!!!!!!
          invigilatorID = form.getlist('invigilatorID','')[i]
          invigilatorUpdate = Invigilator.objects.get(id = invigilatorID)
          invigilatorUpdate.firstname = form.getlist('firstname','')[i]
          invigilatorUpdate.surname = form.getlist('surname','')[i]
          invigilatorUpdate.grade = int(form.getlist('grade','')[i])
          invigilatorUpdate.inv_reg = form.getlist('inv_reg','')[i]
          invigilatorUpdate.phone_h = form.getlist('phone_h','')[i]
          invigilatorUpdate.phone_w = form.getlist('phone_w','')[i]
          invigilatorUpdate.fax_h = form.getlist('fax_h','')[i]
          invigilatorUpdate.fax_w = form.getlist('fax_w','')[i]
          invigilatorUpdate.email = form.getlist('email','')[i]
          invigilatorUpdate.responsible = form.getlist('responsible','')[i]
          invigilatorUpdate.save()
       
    c = {'invigilators':invigilators, 'grades':range(8,13)} #Sends back list of invigilators and grade options
    c.update(csrf(request))
    return render_to_response('invigilators.html', c,context_instance=RequestContext(request))

#*****************************************
# Register Students   
#User can register 5 students per grade and 5 pairs per grade 
@login_required
def newstudents(request):
    error = " "
    if request.method == 'POST':  # If the form has been submitted...
       
        form = (request.POST) # A form bound to the POST data

        #Registering per grade
        for grade in range (8,13):
          
          #Registering the different pairs
          #Information is set to null, only school name is given and reference
          #Reference if the ID of the first person in the pair
          for p in range(int(form.getlist("pairs",'')[grade-8])):
            firstname = ''
            surname = ''
            language = form.getlist('language','')[0]
            reference = 1234
            school = School.objects.get(pk=int(form.getlist('school','')[0]))
            sex = '' 
            registered_by =  User.objects.get(pk=int(form.getlist('registered_by','')[p]))          
            query = SchoolStudent(firstname = firstname , surname = surname, language = language,reference = reference,
                    school = school, grade = grade , sex = sex, registered_by= registered_by)
            query.save()
            query.reference=query.id
            query.save()
            query1 = SchoolStudent(firstname = firstname , surname = surname, language = language,reference = query.id,
                    school = school, grade = grade , sex = sex, registered_by= registered_by)
            query1.save()   

        #Registering students, maximum number of students 25
        #Returns an error if information entered incorrectly         
        try:
          for i in range (25):
            if form.getlist('firstname','')[i] == u'': continue
            firstname = form.getlist('firstname','')[i]
            surname = form.getlist('surname','')[i]
            language = form.getlist('language','')[0]
            reference = 1234
            school = School.objects.get(pk=int(form.getlist('school','')[0]))
            grade = form.getlist('grade','')[i]
            sex = form.getlist('sex','')[i]  
            registered_by =  User.objects.get(pk=int(form.getlist('registered_by','')[i]))          
            query = SchoolStudent(firstname = firstname , surname = surname, language = language,reference = reference,
                    school = school, grade = grade , sex = sex, registered_by= registered_by)
            query.save()
            query.reference=query.id
            query.save()
          return render_to_response('submitted.html', {'type':'Student'}) # Redirect after POST
        except Exception as e:
              error = "Incorrect information inserted into fields. Please insert correct information"
    else:
        form = StudentForm() # An unbound form
        

    schoolOptions = School.objects.all()
    c = {'type':'Students', 'schools':schoolOptions, 'entries_per_grade':range(5), 'pairs_per_grade':range(6), 'grades':range(8,13), 'error':error}
    c.update(csrf(request))
    return render_to_response('newstudents.html', c, context_instance=RequestContext(request))


#*****************************************
#Register Schools
#Registers one school at a time
@login_required
def newschools (request):
  error = " "
  if request.method == 'POST': # If the form has been submitted...
        form = (request.POST) # A form bound to the POST data
        
        #Registers school, returns an error if information is entered incorrectly
        try:
          for i in range (1):
              if form.getlist('name','')[i] == u'': continue
              name = form.getlist('name','')[i]
              key = 123 
              language = form.getlist('language','')[i]
              address = form.getlist('address','')[i]
              phone = form.getlist('phone','')[i]
              fax = form.getlist('fax','')[i]
              contact = form.getlist('contact','')[i]
              email = form.getlist('email','')[i]
              registered_by =  User.objects.get(pk=int(form.getlist('registered_by','')[i]))
              
              query = School(name = name ,key = key ,  language = language  ,
                  address = address, phone = phone , fax = fax, contact = contact , email = email, registered_by= registered_by)
              query.save()
              query.key=query.id
              query.save()

          return render_to_response('submitted.html', {'type':'School'}) # Redirect after POST
        except Exception as e:
              error = "Incorrect information inserted into fields. Please insert correct information"
  else:
        form = SchoolForm() # An unbound form
  

  c = {'type':'Schools', 'range':range(1), 'error':error}
  c.update(csrf(request))

  return render_to_response('newschools.html', c,context_instance=RequestContext(request))


#******************************************
#Register Invigilators
#Register maximum of 4 invigilators at a time
@login_required
def newinvigilators (request):
  error = " "
  if request.method == 'POST': # If the form has been submitted...
        form = (request.POST) # A form bound to the POST data

        #Returns error if information entered incorrectly
        try:
          for i in range (4):
              if form.getlist('firstname','')[i] == u'': continue
              school = School.objects.get(pk=int(form.getlist('school','')[i]))
              firstname = form.getlist('firstname','')[i]
              surname = form.getlist('surname','')[i]
              grade = form.getlist('grade','')[i]
              inv_reg = form.getlist('inv_reg','')[i]
              phone_h = form.getlist('phone_h','')[i]
              phone_w = form.getlist('phone_w','')[i]
              fax_h = form.getlist('fax_h','')[i]
              fax_w = form.getlist('fax_w','')[i]
              email = form.getlist('email','')[i]
              responsible = form.getlist('responsible','')[i]
              registered_by =  User.objects.get(pk=int(form.getlist('registered_by','')[i]))
                          
              query = Invigilator(school = school , firstname = firstname,surname = surname, grade = grade ,
                  inv_reg = inv_reg, phone_h = phone_h , phone_w = phone_w, 
                  fax_h = fax_h, fax_w = fax_w , email = email, responsible = responsible, registered_by= registered_by)
              query.save()

          return render_to_response('submitted.html', {'type':'Invigilator'}) # Redirect after POST
        except Exception as e:
              print e
              error = "Incorrect information inserted into fields. Please insert correct information"
  else:
        form = InvigilatorForm() # An unbound form
  schoolOptions = School.objects.all()

  c = {'schools':schoolOptions, 'range':range(4), 'grades':range(8,13), 'error':error} #******ADD RANGE

  c.update(csrf(request))
  return render_to_response('newinvigilators.html', c,context_instance=RequestContext(request))


#******************************************  
