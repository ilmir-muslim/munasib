from django.urls import path
from .views import CheckAdminsRightsView, CheckTelegramIdView, OperationList, Positions, RecordOperationView, RegisterNewUserView, StatusWindowView, WorksDoneTodey


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
    path("status_window/<int:id_telegram>/", StatusWindowView.as_view(), name="status_window"),
    path("works_done_today/<int:id_telegram>/", WorksDoneTodey.as_view(), name="works_done_today"),
    path('operations/', OperationList.as_view(), name='operations'),
]
