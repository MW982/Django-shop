from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
		path('register/', views.registerView, name='register'),
		path('login/', views.loginView, name='login'),
		path('account/', views.accountView, name='account'),
		path('logout/', views.logoutView, name='logout'),
		path('foruser/', views.forgotUserView, name='forgotUser'),
		path('forpass/', views.forgotPassView,name='forgotPass'),
		path('forpass/<int:k_user>', views.changePassView, name='changePass'),
        path('active/<uuid:activateUUID>', views.activateView, name='activate'),
		path('forpass/<uuid:resetUUID>', views.resetPassView, name='resetPass')
]


