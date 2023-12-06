from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView, FormView
from .forms import *
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests

from isodate import parse_duration
from django.conf import settings
from django.shortcuts import redirect

class NiveauListView(ListView):
    context_object_name = 'niveaux'
    model = Categories
    template_name = 'programme/niveaulist.html'

def dashboard(request):
    matieres = Matiere.objects.all()
    form = MatiereFilterForm(request.GET)
    categories = request.GET.getlist('categories')
    if categories:
        matieres = matieres.filter(categorie__in=categories)

    query = request.GET.get('query')
    if query:
        matieres = matieres.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query) |
            Q(categorie__nom__icontains=query)
        )

    paginator = Paginator(matieres, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'matieres': page_obj,
        'form': form,
    }
    
    return render(request, 'programme/niveaulist.html', context)


class LessonListView(DetailView):
    context_object_name = 'matieres'
    model = Matiere
    template_name = 'programme/lessonlist.html'


class LessonListViewDetail(DetailView, FormView):
    context_object_name = 'lesson'
    model = Lesson
    template_name = 'programme/lessonlistdetail.html'
    form_class = ComForm
    second_form_class = RepForm

    def get_context_data(self, **kwargs):
        context = super(LessonListViewDetail, self).get_context_data(**kwargs)

        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()

        return context  



    def form_valid(self, form):
            self.object = self.get_object()
            fd = form.save(commit=False)
            fd.auteur = self.request.user
            #fd.nom_lesson = self.object.comments.nom
            fd.nom_lesson_id = self.object.id
            fd.save()
            return HttpResponseRedirect(self.get_success_url())


    def form_valid2(self, form):
        self.object = self.get_object()
        fd = form.save(commit=False)
        fd.auteur = self.request.user
        fd.nom_comm_id = self.request.POST.get('comment_id',)
        fd.save()   
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        self.object = self.get_object()
        categorie = self.object.categorie
        matiere = self.object.matiere
        return reverse_lazy('programme:lessonlistdetail', kwargs={
            'categorie':categorie,
            'matiere':matiere,
            'slug':self.object.slug
        })


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.form_class
            form_name = 'form'

        else:
            form_class = self.second_form_class
            form_name = 'form2'  
        form = self.get_form(form_class)

        if form_name=='form' and form.is_valid():
            print('nouvea commentaire')
            return self.form_valid(form)

        if form_name=='form2' and form.is_valid():
            print('nouvelle reponse')
            return self.form_valid2(form)  

class LessonCreateView(CreateView):
    form_class = LessonForm
    context_object_name = 'matieres'
    model = Matiere
    template_name = 'programme/lessoncreate.html' 

    def get_success_url(self):
        self.object = self.get_object()
        categorie = self.object.categorie
        return reverse_lazy('programme:lessonlist', kwargs={'categorie':categorie, 'slug':self.object.slug})

    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        ls = form.save(commit=False)
        ls.creer_par = self.request.user
        ls.categorie = self.object.categorie
        ls.matiere = self.object
        ls.save()
        return HttpResponseRedirect(self.get_success_url())

class LessonUpdateView(UpdateView):
    fields = ('nom', 'position', 'pdf', 'fpe')
    context_object_name = 'lesson'
    model = Lesson
    template_name = 'programme/lessonupdate.html'

class LessonDeleteView(DeleteView):
    model = Lesson
    context_object_name = "lesson"
    template_name = 'programme/lessondelete.html'
    
    def get_success_url(self):
        categorie = self.object.categorie
        matiere = self.object.matiere
        return reverse_lazy("programme:lessonlist", kwargs={'categorie':categorie, 'slug':matiere.slug})


def bibliotheques(request):
    matieres = Matiere.objects.all()
    form = MatiereFilterForm(request.GET)
    categories = request.GET.getlist('categories')
    if categories:
        matieres = matieres.filter(categorie__in=categories)

    query = request.GET.get('query')
    if query:
        matieres = matieres.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query) |
            Q(categorie__nom__icontains=query)
        )

    paginator = Paginator(matieres, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'matieres': page_obj,
        'form': form,
    }
    
    return render(request, 'programme/Bibliotheque/bibliotheques.html', context)

from django.shortcuts import render
from django.db.models import Q
from .models import Epreuve

def banque(request,activated=None):
    epreuves = Epreuve.objects.all()
    
    matieres = request.GET.getlist('matieres')
    annees = request.GET.getlist('annees')
    ecoles = request.GET.getlist('ecoles')
    
    if matieres:
        epreuves = epreuves.filter(nom__in=matieres)
    
    if annees:
        epreuves = epreuves.filter(annee__in=annees)
    
    if ecoles:
        epreuves = epreuves.filter(ecole__in=ecoles)
    
     # Get distinct values for matiere, ecole, and annee
    available_matieres = Epreuve.objects.values_list('nom', flat=True).distinct()
    available_ecoles = Epreuve.objects.values_list('ecole', flat=True).distinct()
    available_annees = Epreuve.objects.values_list('annee', flat=True).distinct()
    
    paginator = Paginator(epreuves, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'epreuves': page_obj,
        'available_matieres': available_matieres,
        'available_ecoles': available_ecoles,
        'available_annees': available_annees
    }
    
    # Check the condition based on the 'activated' parameter
    if activated == 1:  # For example, if activated=1, render the first template
        return render(request, 'programme/back/banque-back.html', context)
    else:
        return render(request, 'programme/Bibliotheque/banque.html', context)



#def banques(request):
 #   return render(request, 'programme/banque.html')

def calendar(request):
    return render(request, 'programme/calendar.html')

def comingsoon(request):
    return render(request, 'programme/commingsoon.html')


def searchf(request):
    query = request.GET.get('query')
    results = []
    if query:
        results = Matiere.objects.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query) |
            Q(categorie__nom__icontains=query)
        )
    return render(request, 'programme/bibliotheques.html', {'matieres':results})


def websearchf(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        page = request.GET.get('page', 1)
        if not query:
            return render(request, 'programme/search.html')
        
        url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI"
        headers = {
            "X-RapidAPI-Key": "d4d95eb11dmshbc1f84ada938c15p153c6fjsn211b5fa53c01",
            "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
        }
        params = {
            "q": query,
            "pageNumber": page,
            "pageSize": 2,
            "autoCorrect": "true"
        }
        response = requests.request("GET", url, headers=headers, params=params)
        results = response.json().get('value', [])
        return render(request, 'programme/search.html', {'query': query, 'results': results})
    else:
        return render(request, 'programme/search.html')
    
def videos(request):
    videos = []

    search_query = "Learn python, computer science and maths"
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    if request.method == 'POST':
        search_query = request.POST.get('search', None)
        if not search_query:
            search_query = "Learn python, computer science and maths"

    search_params = {
                'part' : 'snippet',
                'q' : search_query,
                'key' : settings.YOUTUBE_DATA_API_KEY,
                'maxResults' : 90,
                'type' : 'video',
                'videoCategoryId': '27',  # limit to educational videos only
    }

    r = requests.get(search_url, params=search_params)

    results = r.json().get('items', [])

    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])

    if request.POST.get('submit') == 'lucky':
        return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

    video_params = {
                'key' : settings.YOUTUBE_DATA_API_KEY,
                'part' : 'snippet,contentDetails',
                'id' : ','.join(video_ids),
                'maxResults' : 91
    }

    r = requests.get(video_url, params=video_params)

    results = r.json().get('items', [])

    for result in results:
                video_data = {
                    'title' : result['snippet']['title'],
                    'id' : result['id'],
                    'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                    'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                    'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                    'category': result['snippet']['categoryId']
                }

                videos.append(video_data)
    context = {
        'videos': videos
    }

    return render(request, 'programme/Bibliotheque/videos.html', context)




def translate(request):
    output_text = ""
    if request.method == 'POST':
        text = request.POST.get('text')
        source = request.POST.get('source_language')
        target = request.POST.get('target_language')
        payload = "text={}&from={}&to={}&forcehtml=0&forceutf8=0".format(text, source, target)
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": "d4d95eb11dmshbc1f84ada938c15p153c6fjsn211b5fa53c01",
            "X-RapidAPI-Host": "translator101.p.rapidapi.com"
        }

        url = "https://translator101.p.rapidapi.com/api/"

        response = requests.request("POST", url, data=payload, headers=headers)
        if response.ok:
            result = response.json()
            if 'translatedText' in result:
                output_text = result['translatedText']
            else:
                output_text = 'Translation failed'
        else:
            output_text = 'Request failed'

    return render(request, 'programme/translate.html', {'output': output_text})


def mailbox(request):
    return render(request, 'programme/back/mailbox.html')

def code_editor(request):
    return render(request, 'programme/back/code-editor.html')


