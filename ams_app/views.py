from django.shortcuts import render , redirect
from . import models
from django.contrib import messages
import bcrypt
from datetime import datetime 
from django.http import HttpResponse
# from rest_framework import serializers
from django.http import JsonResponse



# Create your views here.
def index(request): # the main page for all
    if 'admin_id' in request.session:
        return redirect('/dashboard')
    else:
        clinics = models.Clinic.objects.all()
        context = {
            'clinics': clinics
        }   
        return render(request, 'index.html' , context)

def dashboard(request): #the page only for the ADMIN
    if 'admin_id' not in request.session:
        return redirect('/')
    else:
        clinics = models.Clinic.objects.all()
        apointments = models.Appointment.objects.all()
        pacients = models.Pacient.objects.all()
        doctors = models.Doctor.objects.all()
        today_appointments = models.get_today_appointments()
        # all_avalable_dates = models.get_all_avalable_dates()
        # print(all_avalable_dates)
        
        context = {
            'clinics': clinics ,
            'apointments' : apointments,
            'pacients' : pacients,
            'doctors' : doctors,
            'today_appointments' : today_appointments,
            # 'all_avalable_dates' : all_avalable_dates,

        }
        return render(request, 'dashboard.html' , context)

def register(request): # to register as Admin
    return render(request, 'admin_register.html')

def login(request):# to log in as Admin
    return render(request, 'admin_login.html')

def logout(request):
    request.session.clear()
    return redirect('/')

def add_doctor_page(request): # open the page to add doctor
    if 'admin_id' not in request.session:
        return redirect('/')
    context = {
        'clinics': models.Clinic.objects.all()
    }
    return render(request, 'add_doctor.html' ,context)

def add_clinic_page(request):
    if 'admin_id' not in request.session:
        return redirect('/')
    return render(request, 'add_clinic.html')

def add_pacient_page(request):
    if 'admin_id' not in request.session:
        return redirect('/')
    return render(request, 'add_pacient.html')

def pacients_page(request):
    if 'admin_id' not in request.session:
        return redirect('/')
    else:
        pacients = models.Pacient.objects.all()
        context = {
            'pacients': pacients
        }
        return render(request, 'pacients.html',context)

def appointment(request, id):
    if 'admin_id' not in request.session:
        return redirect('/')
    else:
        # %dT%H:%M
        # we calculate the working ours
        min_datetime = models.date_time_min().strftime('%Y-%m-%dT%H:%M')
        max_datetime = models.date_time_max().strftime('%Y-%m-%dT%H:%M') 
        
        pacient = models.Pacient.objects.get(id=id)
        clinics = models.Clinic.objects.all()
        
        context = {
            'pacient': pacient,
            'clinics': clinics,
            'min_datetime': min_datetime,
            'max_datetime': max_datetime,
            
        }
        return render(request, 'apointment.html', context)



def aboutus(request):
    return render(request, 'aboutus.html')

# --------------------------------------------------------------------

def admin_register(request):
    errors = models.Admin.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value , extra_tags = 'admin_registration' )
            
        return redirect('/registr_admin')
    else:
        admin_first_name = request.POST['admin_first_name']
        admin_last_name = request.POST['admin_last_name']
        admin_email = request.POST['admin_email']
        admin_phone = request.POST['admin_phone']
        admin_password = request.POST['admin_password']
        admin_repete_password = request.POST['admin_repete_password']
        #hash------------
        pw_hash = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt()).decode()
        pw_hash_confirm = bcrypt.hashpw(admin_repete_password.encode(), bcrypt.gensalt()).decode()
        #hash------------
        models.create_admin(admin_first_name, admin_last_name, admin_email, admin_phone,  pw_hash, pw_hash_confirm) 
        messages.success(request, "You have successfully registered as Admin!")
        return redirect('/registr_admin')


def admin_login(request):
    errors = models.Admin.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_admin')
    else:
        admin_email = request.POST['admin_email'] # here we get the email thet ENSERTED
        admin_password = request.POST['admin_password'] # here we get the password thet ENSERTED
        admin = models.Admin.objects.get(email=admin_email) # here we get the admin by the email from DB
        if bcrypt.checkpw(admin_password.encode(), admin.admin_password.encode()): # here we chick the password 
            request.session['admin_id'] = admin.id
            return redirect('/dashboard')
        else:
            messages.error(request, "Email or Password is incorrect")
        return redirect('/login_admin')


def add_clinic(request):
    errors = models.Clinic.objects.clinic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add_clinic_page')
    else:
        clinic_name = request.POST['the_clinic_name']
        clinic_specialty = request.POST['clinic_specialty']
        clinic_details = request.POST['clinic_details']
        clinic = models.create_a_clinic(clinic_name=clinic_name, clinic_specialty=clinic_specialty, clinic_details=clinic_details)
        messages.success(request, "You have successfully added a clinic!")
        return redirect('/add_clinic_page')

def add_doctor(request):
    errors = models.Doctor.objects.doctor_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add_doctor_page')
    else:
        doctor_first_name = request.POST['doctor_first_name']
        doctor_last_name = request.POST['doctor_last_name']
        doctor_specialty = request.POST['doctor_specialty']
        doctor_phone = request.POST['doctor_phone_number']
        clinic_name = request.POST['clinic_name']
        doctor = models.create_a_doctor(doctor_first_name=doctor_first_name, doctor_last_name=doctor_last_name, doctor_specialty=doctor_specialty, doctor_phone=doctor_phone, clinic_name=clinic_name)
        messages.success(request, "You have successfully added a doctor!")
        return redirect('/add_doctor_page')

def add_pacient(request):
    errors = models.Pacient.objects.pacient_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add_pacient_page')
    else:
        pacient_first_name = request.POST['added_first_name']
        pacient_last_name = request.POST['added_last_name']
        patient_phone_number = request.POST['added_phone_number']
        pacient_identity_number = request.POST['added_identity_number']
        pacient_details = request.POST['added_details']
        pacient = models.create_a_pacient(first_name=pacient_first_name,last_name=pacient_last_name,phone_number=patient_phone_number,identity_number=pacient_identity_number,pacient_details=pacient_details)
        messages.success(request, "Successfully Added !" , extra_tags='pacient_added')
        return redirect('/add_pacient_page')

def add_appointment(request, id):
    errors = models.Appointment.objects.appointment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/appointment/{id}')
    else:
        datetime_object = datetime.strptime(request.POST['appointment_date'], '%Y-%m-%dT%H:%M')
        if datetime_object < datetime.now():
            messages.error(request, "You can't add an appointment in the past" ,extra_tags='wrong_date')
            return redirect(f'/appointment/{id}')
        selected_appointment = request.POST['appointment_date']
        appointment_details = request.POST['appointment_details']
        pacient_id = id
        clinic_name = request.POST['clinic_name']
        apointment = models.create_an_appointment(appointment_date = selected_appointment , appointment_details=appointment_details, pacient_id=pacient_id, clinic_name=clinic_name)
        messages.success(request, "Successfully Added !", extra_tags='appointment_added')
        return redirect(f'/appointment/{id}')

def delete_appointment(request, id):
    appointment = models.Appointment.objects.get(id=id)
    appointment.delete()
    return redirect('/dashboard')

def edit_appointment(request, id):
    appointments = models.Appointment.objects.get(id=id)
    #this line to parse the date to be acceptable by the form
    appointments_date = appointments.appointment_date.strftime('%Y-%m-%dT%H:%M')  
    # the time that we inserted as VALUE of datetime-local in th DOM
    min_datetime = models.date_time_min().strftime('%Y-%m-%dT%H:%M')
    max_datetime = models.date_time_max().strftime('%Y-%m-%dT%H:%M') 
        
    clinics = models.Clinic.objects.all()
    context = {
        'appointments': appointments,
        'clinics': clinics,
        #this line to parse the date to be acceptable by the form
        'appointments_date': appointments_date, 
        'min_datetime': min_datetime,
        'max_datetime': max_datetime,
        }
    print(appointments_date)
    return render(request, 'edit_appointment.html', context )

def update_appointment(request, id):
    errors = models.Appointment.objects.appointment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit_appointment/{id}')
    else:
        datetime_object = datetime.strptime(request.POST['appointment_date'], '%Y-%m-%dT%H:%M')
        if datetime_object < datetime.now():
            messages.error(request, "You can't add an appointment in the past", extra_tags='wrong_date')
            return redirect(f'/edit_appointment/{id}')
        appointment_date = request.POST['appointment_date']
        appointment_details = request.POST['appointment_details']
        clinic_name = request.POST['clinic_name']
        models.update_an_appointment(id, appointment_date, appointment_details, clinic_name)
        messages.success(request, "Successfully Updated !", extra_tags='appointment_updated')
        return redirect(f'/edit_appointment/{id}')

# def start_date():
#     start_of_date = datetime.now().date()
#     return start_of_date

# def time_delta():
#     on_week = start_date() + timedelta(days=7)
#     return on_week






def search(request): # the main view
    if 'admin_id' not in request.session:
        return redirect('/')
    else:
        # search_term = request.POST['search_term']
        # pacients = models.Pacient.objects.filter(first_name__icontains=search_term)
        context = {
            # 'pacients': pacients
        }
        return render(request, 'search.html', context)

def search_results(request): # its a function to get the search value AJAX
    if 'admin_id' not in request.session:
        return redirect('/')
    else:
        if request.is_ajax():
            res = None
            searchValue = request.POST.get('searchValue')
            print(searchValue)
            qs = models.Pacient.objects.filter(patient_first_name__icontains=searchValue)
            if len(qs) > 0 and  len(searchValue) > 0:
                data = []
                for pos in qs:
                    item = {
                        'id': pos.id,
                        'first_name': pos.patient_first_name,
                        'last_name': pos.patient_last_name,
                        'phone_number': pos.patient_phone_number,
                        'identity_number': pos.pacient_identity_number,
                        'details': pos.pacient_details,
                    }
                    data.append(item)
                res = data
            else:
                res = 'No Paicents found ...'
            return JsonResponse({'data': res})
        return JsonResponse({})

def clinicpage(request , id):
    if 'admin_id' not in request.session:
        return redirect('/')
    else:
        clinics = models.Clinic.objects.get(id =  id)
        all_the_appointments = models.Appointment.objects.filter(clinic = id)
        vailable_appointments = models.Appointment.objects.filter(clinic = id, appointment_date__gte = datetime.now())
        all_appointments = all_the_appointments.order_by('appointment_date')
        number_of_appointments = len(all_appointments)
        
        context = {
            'clinics': clinics,
            'all_appointments': all_appointments,
            'vailable_appointments': vailable_appointments,
            'number_of_appointments': number_of_appointments,

        }
        return render(request, 'clinic.html', context)


def reportpage(request ,id ,pacient_id):
    if 'admin_id' not in request.session:
        return redirect('/')
    else:
        pacients = models.Pacient.objects.get(id = pacient_id)
        apointment = models.Appointment.objects.get(id = id)
        context = {
            'pacients': pacients,
            'apointment': apointment,

        }
        return render(request, 'report.html', context)