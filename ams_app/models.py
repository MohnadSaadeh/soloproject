from django.db import models
from datetime import datetime
import re
import datetime

# Create your models here.

#--------------------------------------------------------------------ADMIN-----------------------
class AdminManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['admin_first_name']) < 2:
            errors['admin_first_name'] = "First name should be at least 2 characters"
        if len(postData['admin_last_name']) < 2:
            errors['admin_last_name'] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['admin_email']):
            errors['admin_email'] = "Invalid email address!"
        if len(postData['admin_phone']) < 10:
            errors['admin_phone'] = "Phone number should be at least 10 characters"
        if len(postData['admin_password']) < 8:
            errors['admin_password'] = "Password should be at least 8 characters"
        if postData['admin_repete_password'] != postData['admin_password']:
            errors['admin_repete_password'] = "Passwords do not match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['admin_email']):
            errors['admin_email'] = "Invalid email address!"
        if len(postData['admin_password']) < 8:
            errors['admin_password'] = "Password should be at least 8 characters"
        return errors

class Admin(models.Model):
    admin_first_name = models.CharField(max_length=100)
    admin_last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    admin_password = models.CharField(max_length=100)
    admin_confirm_password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AdminManager()

    def __str__(self):
        return self.name
# Create Admin user
def create_admin(first_name, last_name, admin_email, admin_phone, hash_password, hash_confirm_password):
    admin = Admin.objects.create(admin_first_name=first_name, admin_last_name=last_name,email=admin_email, 
    phone=admin_phone, admin_password=hash_password, admin_confirm_password=hash_confirm_password)
    return admin
#--------------------------------------------------------------------ADMIN-----------------------

#--------------------------------------------------------------------CLINIC-----------------------
class ClinicManager(models.Manager):
    def clinic_validator(self, postData):
        errors = {}
        if len(postData['the_clinic_name']) < 2:
            errors['clinic_name'] = "Clinic name should be at least 2 characters"
        if len(postData['clinic_specialty']) < 2:
            errors['clinic_specialty'] = "Clinic specialty should be at least 2 characters"
        if len(postData['clinic_details']) < 10:
            errors['clinic_details'] = "Clinic details should be at least 2 characters"
        return errors

class Clinic(models.Model):
    clinic_name = models.CharField(max_length=100)
    clinic_specialty = models.CharField(max_length=100)
    clinic_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ClinicManager()
    # doctors : doctor of this clinic
    # appointments : appointments of this clinic
    def __str__(self):
        return self.clinic_name

def create_a_clinic(clinic_name, clinic_specialty, clinic_details):
    clinic = Clinic.objects.create(clinic_name=clinic_name, clinic_specialty=clinic_specialty, clinic_details=clinic_details)
    return clinic

#--------------------------------------------------------------------CLINIC-----------------------

#--------------------------------------------------------------------DOCTOR-----------------------
class DoctorManager(models.Manager):
    def doctor_validator(self, postData):
        errors = {}
        if len(postData['doctor_first_name']) < 2:
            errors['doctor_first_name'] = "First name should be at least 2 characters"
        if len(postData['doctor_last_name']) < 2:
            errors['doctor_last_name'] = "Last name should be at least 2 characters"
        if len(postData['doctor_specialty']) < 2:
            errors['doctor_specialty'] = "Specialty should be at least 2 characters"
        if len(postData['doctor_phone_number']) < 10:
            errors['doctor_phone_number'] = "Phone number should be at least 10 characters"
        if len(postData['clinic_name']) == 0 :
            errors['clinic_name'] = "You should be choose a Clinic"
        return errors

class Doctor(models.Model):
    doctor_first_name = models.CharField(max_length=100)
    doctor_last_name = models.CharField(max_length=100)
    doctor_specialty = models.CharField(max_length=100)
    doctor_phone_number = models.CharField(max_length=100)
    clinic_name = models.ForeignKey(Clinic, related_name="doctors", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DoctorManager()
    # appointments : appointments of this doctor
    # patients : patient of this doctor
    def __str__(self):
        return self.doctor_first_name

def create_a_doctor(doctor_first_name, doctor_last_name, doctor_specialty, doctor_phone,clinic_name):
    doctor = Doctor.objects.create(doctor_first_name=doctor_first_name,
    doctor_last_name=doctor_last_name,
    doctor_specialty=doctor_specialty,
    doctor_phone_number=doctor_phone,
    clinic_name=(Clinic.objects.get(clinic_name=clinic_name) ))
    return doctor
#--------------------------------------------------------------------DOCTOR-----------------------

#--------------------------------------------------------------------PATIENT-----------------------

class PacientManager(models.Manager):
    def pacient_validator(self, postData):
        errors = {}
        if len(postData['added_first_name']) < 2:
            errors['patient_first_name'] = "First name should be at least 2 characters"
        if len(postData['added_last_name']) < 2:
            errors['patient_last_name'] = "Last name should be at least 2 characters"
        if len(postData['added_phone_number']) != 10:
            errors['patient_phone_number'] = "Phone number should be 10 numbers"
        if len(postData['added_identity_number']) != 9:
            errors['pacient_identity_number'] = "Identity number should be 9 numbers"
        if len(postData['added_details']) < 10:
            errors['pacient_details'] = "Details should be at least 10 characters"
        return errors

class Pacient(models.Model):
    patient_first_name = models.CharField(max_length=100)
    patient_last_name = models.CharField(max_length=100)
    patient_phone_number = models.CharField(max_length=100)
    pacient_identity_number = models.CharField(max_length=100)
    pacient_details = models.TextField()
    doctor = models.ManyToManyField(Doctor, related_name="pacients")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # appointments : appointments of this pacient
    # doctors : doctor of this pacient
    objects = PacientManager()
    def __str__(self):
        return self.patient_first_name

def create_a_pacient(first_name,last_name,phone_number, identity_number, pacient_details):
    pacient = Pacient.objects.create(patient_first_name=first_name,
    patient_last_name=last_name,
    patient_phone_number=phone_number,
    pacient_identity_number=identity_number,
    pacient_details=pacient_details)
    return pacient

#--------------------------------------------------------------------PATIENT-----------------------

# if not EMAIL_REGEX.match(postData['admin_email']):
#             errors['admin_email'] = "Invalid email address!"
#--------------------------------------------------------------------APOINTMENTS-----------------------

class AppointmentManager(models.Manager):
    def appointment_validator(self, postData):
        # datetime_object = datetime.strptime(postData['appointment_date'], '%Y-%m-%dT%H:%M')
        # DATE_REGEX = re.compile(r'^(?:202\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])T(?:8|9|10|11|12|13|14|15|16):[0-5]\d)$')
        # (?:202\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]): Matches the date part in the format YYYY-MM-DD.
        # T: Matches the literal 'T' character which separates the date and time parts.
        # (?:09|1[0-5]): Matches the hour part between 09 and 15.
        # :[0-5]\d: Matches the minutes part (00 to 59).
        # $: Asserts the end of the string.
        DATE_REGEX = re.compile(r'^(?:202\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])T(?:09|1[0-5]):[0-5]\d)$')
        errors = {}
        if len(postData['appointment_details']) < 5:
            errors['appointment_details'] = "Details should be at least 5 characters"
        if not DATE_REGEX.match(postData['appointment_date']):
            errors['appointment_date'] = "You Have to chose whith the working Hours"
        if postData['clinic_name'] == "- Select Clinic -"   :
            errors['clinic_name'] = "You should be choose a Clinic"
        return errors

class Appointment(models.Model):
    appointment_date = models.DateTimeField()
    appointment_details = models.TextField()
    pacient = models.ForeignKey(Pacient, related_name="appointments", on_delete = models.CASCADE)
    clinic = models.ForeignKey(Clinic, related_name="appointments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()

    def __str__(self):
        return self.appointment_date

def create_an_appointment(appointment_date, appointment_details, pacient_id, clinic_name):
    clinic_id = Clinic.objects.get(id=Clinic.objects.get(clinic_name=clinic_name).id)
    appointment = Appointment.objects.create(appointment_date=appointment_date,
    appointment_details=appointment_details,
    pacient=(Pacient.objects.get(id=pacient_id) ),
    clinic= clinic_id )
    return appointment


def get_today_appointments():
    return Appointment.objects.filter(appointment_date__date=datetime.date.today())



def update_an_appointment(id, appointment_date, appointment_details, clinic_name):
    clinic_id = Clinic.objects.get(id=Clinic.objects.get(clinic_name=clinic_name).id)
    appointment = Appointment.objects.get(id=id)
    appointment.appointment_date = appointment_date
    appointment.appointment_details = appointment_details
    appointment.clinic = clinic_id
    appointment.save()
    return appointment



#--------------------------------------------------------------------APOINTMENTS----------------------- 


#--------------------------------------------------------------------WORKING OURS----------------------- 

def date_time_min():
    working_hours_start = "09:00"
    min_datetime = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(working_hours_start, "%H:%M").time())
    return min_datetime

def date_time_max():
    working_hours_end = "17:00"
    add_one_week = datetime.timedelta(days=7)
    max_datetime = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(working_hours_end, "%H:%M").time())+add_one_week
    return max_datetime


# def get_all_avalable_dates():
#     # # Get all existing datetime values from the database
#     # Get the start date (today)
#     start_date = datetime.now().date()

#     # Get the end date (today + 7 days)
#     end_date = start_date + timedelta(days=7)

#     # Get all existing datetime values from the database within the date range
#     existing_datetimes = Appointment.objects.filter(appointment_date__range=(start_date, end_date)).values_list('appointment_date', flat=True)

#     # Generate all dates within the date range (today to today + 7 days)
#     all_dates = [start_date + timedelta(days=i) for i in range(8)]

#     # Exclude dates that already exist in the database
#     available_dates = [date for date in all_dates if date not in existing_datetimes]
#     return available_dates
