from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
		path('register/', views.register, name='register'),
		path('login/', views.loginView, name='login'),
		path('account/', views.account, name='account'),
		path('logout/', views.logoutView, name='logout'),
		path('foruser/', views.forgotUser, name='forgotUser'),
		path('forpass/', views.forgotPass,name='forgotPass'),
		path('forpass/<int:k_user>', views.changePass, name='changePass'),
    path('active/<uuid:activateUUID>', views.activate, name='activate'),
		path('forpass/<uuid:resetUUID>', views.resetPass, name='resetPass')
]


