from django.urls import path
from programme.views import *
app_name = "programme"

urlpatterns = [
    path('', NiveauListView.as_view(), name="niveaulist"),
    path('bibliotheques', bibliotheques, name="bibliotheques"),
    path('bibliotheques/banque', banque, name="banque"),
    path('bibliotheques/banque/<int:activated>/', banque, name="banque"),
    path('bibliotheques/videos', videos, name="videos"),
    path('bibliotheques/search/', searchf, name='search'),
    path('websearch/', websearchf, name='websearch'),
    path('<slug:slug>',dashboard, name="matierelist"),
    path('translate/', translate, name='translate'),
    path('<str:categorie>/<slug:slug>/', LessonListView.as_view(), name="lessonlist"),
    path('/calendar', calendar, name="calendar"),
    path('/comingsoon', comingsoon, name="comingsoon"),
    path('mailbox/', mailbox, name='mailbox'),
    path('code_editor/', code_editor, name='code_editor'),
    path('translate/', translate, name='translate'),
    path('<str:categorie>/<str:slug>/create/', LessonCreateView.as_view(), name="lessoncreate"),
    path('<str:categorie>/<str:matiere>/<slug:slug>/', LessonListViewDetail.as_view(), name="lessonlistdetail"),
    path('<str:categorie>/<str:matiere>/<slug:slug>/update', LessonUpdateView.as_view(), name="lessonupdate"),
    path('<str:categorie>/<str:matiere>/<slug:slug>/delete', LessonDeleteView.as_view(), name="lessondelete"),

]