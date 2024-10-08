from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import DoctorForm, DoctorLoginForm, PatientForm
from .models import Doctor, Patient
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Timeline


# Doctor-Login
def index(request):
   
   if request.method == 'POST':
      form = DoctorLoginForm(data = request.POST)
      if form.is_valid():
         username = form.cleaned_data['username']
         password = form.cleaned_data['password']

         user = authenticate(request, username=username, password=password)
         if user is not None:
               login(request, user)
               return render(request, 'home.html')
      return render(request, 'index.html', context={'form': form, 'error': 'Invalid username or password'})
         
   else:
      form = DoctorLoginForm()
      return render(request, 'index.html', context={'form': form, 'error': ''})

def signup(request):
   # if request.user.is_authenticated:
   #    return HttpResponse(reverse('home'))
   error = ''
   form = DoctorForm()
   if request.method == 'POST':
      form = DoctorForm(request.POST)
      print(form['username'],form['email'],form['password1'],form['password2'],form['phone'],form['specialization'])
      if form.is_valid():

         print(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password1'],form.cleaned_data['password2'],form.cleaned_data['phone'],form.cleaned_data['specialization'])
         user = form.save()
         user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
         if user is not None:
               login(request, user)
               return render(request, 'home.html')
         else:
            return HttpResponseRedirect(reverse('index.html'))
      else:
         if User.objects.filter(email=request.POST['email']).exists():
            error = 'Doctor already exists'
         else:
            error = 'Your password is not strong enough or both password must be same'
   
   return render(request, 'signup.html',context={'form': form,'error': error})

@login_required
def home(request):
   return render(request, 'home.html')

import time
@login_required
def timeline(request):
   if request.method == "GET":
      return render(request, 'timeline.html',{'text':'','time':''})
   text = request.POST.get('transcript')  
   context = {'text': text,'time':time.time()}
   print(context)
   return render(request, 'timeline.html', context)

@login_required
def analytics(request):
   return render(request, 'analytics.html')

def about(request):
   return render(request, 'about.html')

def contact(request):
   return render(request, 'contact.html')

@login_required
def patientAdmit(request):
   if request.method == 'POST':
      form = PatientForm(request.POST)
      if form.is_valid():
         form.save()
         return render(request, 'home.html')
      else:
         error = form.errors
         print(form.errors)
   else:
      form = PatientForm()
   return render(request, 'patientAdmit.html',context={'form': form,'error': 'error'})

@login_required
def patientReAdmit(request):
   return render(request, 'patientReAdmit.html')

@login_required
def live(request):
   return render(request, 'graphs2.html')



#loading trained_model
import joblib as jb
model = jb.load('trained_model')

@login_required
def predict(request):
   if request.method == 'POST':
      pass
   return render(request,'predict.html')

def checkdisease(request):

  diseaselist=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes ',
  'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
  'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
  'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
  'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
  'Arthritis', '(vertigo) Paroymsal  Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']


  symptomslist=['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
  'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination',
  'fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy',
  'patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating',
  'dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes',
  'back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
  'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
  'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
  'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
  'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
  'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
  'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
  'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
  'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
  'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
  'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
  'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
  'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
  'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
  'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
  'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
  'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
  'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
  'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
  'yellow_crust_ooze']

  alphabaticsymptomslist = sorted(symptomslist)

  


  if request.method == 'GET':
    
     return render(request,'checkdisease.html', {"list2":alphabaticsymptomslist})




  elif request.method == 'POST':
       
      ## access you data by playing around with the request.POST object
      
      inputno = int(request.POST["noofsym"])
      print(inputno)
      if (inputno == 0 ) :
          return JsonResponse({'predicteddisease': "none",'confidencescore': 0 })
  
      else :

        psymptoms = []
        psymptoms = request.POST.getlist("symptoms[]")
       
        print(psymptoms)

      
        """      #main code start from here...
        """
      

      
        testingsymptoms = []
        #append zero in all coloumn fields...
        for x in range(0, len(symptomslist)):
          testingsymptoms.append(0)


        #update 1 where symptoms gets matched...
        for k in range(0, len(symptomslist)):

          for z in psymptoms:
              if (z == symptomslist[k]):
                  testingsymptoms[k] = 1


        inputtest = [testingsymptoms]

        print(inputtest)
      

        predicted = model.predict(inputtest)
        print("predicted disease is : ")
        print(predicted)

        y_pred_2 = model.predict_proba(inputtest)
        confidencescore=y_pred_2.max() * 100
        print(" confidence score of : = {0} ".format(confidencescore))

        confidencescore = format(confidencescore, '.0f')
        predicted_disease = predicted[0]

        

        #consult_doctor codes----------

        #   doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
        #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]
        

        Rheumatologist = [  'Osteoarthristis','Arthritis']
       
        Cardiologist = [ 'Heart attack','Bronchial Asthma','Hypertension ']
       
        ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo','Hypothyroidism' ]

        Orthopedist = []

        Neurologist = ['Varicose veins','Paralysis (brain hemorrhage)','Migraine','Cervical spondylosis']

        Allergist_Immunologist = ['Allergy','Pneumonia',
        'AIDS','Common Cold','Tuberculosis','Malaria','Dengue','Typhoid']

        Urologist = [ 'Urinary tract infection',
         'Dimorphic hemmorhoids(piles)']

        Dermatologist = [  'Acne','Chicken pox','Fungal infection','Psoriasis','Impetigo']

        Gastroenterologist = ['Peptic ulcer diseae', 'GERD','Chronic cholestasis','Drug Reaction','Gastroenteritis','Hepatitis E',
        'Alcoholic hepatitis','Jaundice','hepatitis A',
         'Hepatitis B', 'Hepatitis C', 'Hepatitis D','Diabetes ','Hypoglycemia']
         
        if predicted_disease in Rheumatologist :
           consultdoctor = "Rheumatologist"
           
        if predicted_disease in Cardiologist :
           consultdoctor = "Cardiologist"
           

        elif predicted_disease in ENT_specialist :
           consultdoctor = "ENT specialist"
     
        elif predicted_disease in Orthopedist :
           consultdoctor = "Orthopedist"
     
        elif predicted_disease in Neurologist :
           consultdoctor = "Neurologist"
     
        elif predicted_disease in Allergist_Immunologist :
           consultdoctor = "Allergist/Immunologist"
     
        elif predicted_disease in Urologist :
           consultdoctor = "Urologist"
     
        elif predicted_disease in Dermatologist :
           consultdoctor = "Dermatologist"
     
        elif predicted_disease in Gastroenterologist :
           consultdoctor = "Gastroenterologist"
     
        else :
           consultdoctor = "other"


        request.session['doctortype'] = consultdoctor 

        patientusername = 'Jhon Doe' #request.session['patientusername']
        puser = Patient.objects.get(Patient_Name=patientusername)
     

        #saving to database.....................

        patient = puser
        diseasename = predicted_disease
        no_of_symp = inputno
        symptomsname = psymptoms
        confidence = confidencescore

      #   diseaseinfo_new = diseaseinfo(patient=patient,diseasename=diseasename,no_of_symp=no_of_symp,symptomsname=symptomsname,confidence=confidence,consultdoctor=consultdoctor)
      #   diseaseinfo_new.save()
        

      #   request.session['diseaseinfo_id'] = diseaseinfo_new.id

      #   print("disease record saved sucessfully.............................")

        return JsonResponse({'predicteddisease': predicted_disease ,'confidencescore':confidencescore , "consultdoctor": consultdoctor})

import assemblyai as aai

aai.settings.api_key = "d6f5f88ea49548ab88a9465c686b61bb"
transcriber = aai.Transcriber()


@login_required
def voiceInput(request):
   if request.method == 'POST':
      pass
   # transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

   # print(transcript.text)
   return render(request,'voiceInput.html')


from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect




@login_required
@csrf_protect
def transcribe_audio(request):

   aai.settings.api_key = "d6f5f88ea49548ab88a9465c686b61bb"
   transcriber = aai.Transcriber()
   transcript = transcriber.transcribe("C:/Users/Shrikanth/Music/recording.webm")
   print(f'Transcription result: {transcript.text}')
   count = 0
   while count < 100:
      count += 1
   return JsonResponse({'transcript': transcript.text})

@login_required
def timeline_data(request):

   t = time.localtime()
   context = {'text': "Patient Responed Well",'time': time.strftime("%H:%M PM",t)}
   return render(request,'timeline.html', context)
