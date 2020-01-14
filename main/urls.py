from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("account/", views.account_view, name="account"),
    path("account/settings/", views.account_settings_view, name="accountSettings"),
    path(
        "account/transactions/",
        views.account_transactions_view,
        name="accountTransactions",
    ),
    path(
        "account/transactions/<int:trans_id>/",
        views.transaction_detail_view,
        name="transactionDetail",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("foruser/", views.forgot_user_view, name="forgotUser"),
    path("forpass/", views.forgot_pass_view, name="forgotPass"),
    path("forpass/<int:k_user>/", views.change_pass_view, name="changePass"),
    path("active/<uuid:activateUUID>/", views.activate_view, name="activate"),
    path("forpass/<uuid:resetUUID>/", views.reset_pass_view, name="resetPass"),
]
