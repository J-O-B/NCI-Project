from django.urls import path
from .views import Index, SaveData, EditProfile, EmailPin, ProfileView, addIP, addDevice, ListCredentialView, AddCredentialView, ViewCredential

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('edit-profile', EditProfile.as_view(), name='edit_profile'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('add-ip', addIP.as_view(), name='add_ip'),
    path('add-device', addDevice.as_view(), name='add_device'),
    path('credentials', ListCredentialView.as_view(), name='creds'),
    path('add-credential', AddCredentialView.as_view(), name='add_creds'),
    path('request_pin', EmailPin.as_view(), name='req_pin'),
    path('confirmation/<str:id>', SaveData.as_view(), name='twofa'),
    path('view-credential/<str:id>', ViewCredential.as_view(), name='view_cred'),
]