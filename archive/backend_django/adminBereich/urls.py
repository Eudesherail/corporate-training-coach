from django.urls import path
from .views import save_documents, edit_documents, load_documents, delete_document

urlpatterns = [
    path('Admin/upload/', save_documents, name='save_documents'),
    path('Admin/edit/', edit_documents, name='edit_document'),
    path('Admin/laden/<str:username>/', load_documents, name='load_document'),
    path('Admin/loeschen/<str:id>/', delete_document, name='delete_document'),

]