from django.urls import path
from .views import CheckAdminsRightsView, CheckTelegramIdView, Positions, RecordOperationView, RegisterNewUserView


urlpatterns = [
    path("record_operation/", RecordOperationView.as_view(), name="record_operation"),
    path(
        "check_telegram_id/<int:id_telegram>/",
        CheckTelegramIdView.as_view(),
        name="check_telegram_id",
    ),
    path("register_user/", RegisterNewUserView.as_view(), name="register_user"),
    path(
        "check_admins_rights/<int:id_telegram>/",
        CheckAdminsRightsView.as_view(),
        name="check_admins_rights",
    ),
    path("positions/", Positions.as_view(), name="positions"),
]
