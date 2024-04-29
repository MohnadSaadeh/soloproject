from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard),
    path('registr_admin', views.register),
    path('login_admin', views.login),
    path('logout', views.logout),
    
    path('add_doctor_page', views.add_doctor_page),# go to doctor page to add a Doctor
    path('add_clinic_page', views.add_clinic_page),
    path('add_pacient_page', views.add_pacient_page),
    path('pacients_page', views.pacients_page),

    path('admin_registr' ,views.admin_register ), #will sti in the same page
    path('admin_login', views.admin_login),
    

    path('add_clinic', views.add_clinic), #add clinic to the DB
    path('add_doctor', views.add_doctor),
    path('add_pacient', views.add_pacient),
    path('appointment/<int:id>', views.appointment),
    path('add_appointment/<int:id>', views.add_appointment),

    path('aboutus', views.aboutus),

    #path('delete_pacient/<int:id>', views.delete_pacient),
    path('deleteappointment/<int:id>', views.delete_appointment),

    path('edit_appointment/<int:id>', views.edit_appointment),
    path('update_appointment/<int:id>', views.update_appointment),


    path('searchpage', views.search),
    path('search', views.search_results , name='search'),# ajax

    path('clinicpage/<int:id>', views.clinicpage),
    path('report_page/<int:id>/<int:pacient_id>', views.reportpage),


    ]