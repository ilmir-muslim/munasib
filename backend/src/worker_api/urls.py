from django.urls import path
from .views import (
    CheckAdminsRightsView,
    CheckTelegramIdView,
    OperationList,
    Positions,
    RecordOperationView,
    RegisterNewUserView,
    StatusWindowView,
    WorkersStaticInfo,
    WorksDoneToday,
)


urlpatterns = [
    path("record_operation/", RecordOperationView.as_view(), name="record_operation"),
    path(
        "check_telegram_id/<int:telegram_id>/",
        CheckTelegramIdView.as_view(),
        name="check_telegram_id",
    ),
    path("register_user/", RegisterNewUserView.as_view(), name="register_user"),
    path(
        "check_admins_rights/<int:telegram_id>/",
        CheckAdminsRightsView.as_view(),
        name="check_admins_rights",
    ),
    path("positions/", Positions.as_view(), name="positions"),
    path(
        "status_window/<int:telegram_id>/",
        StatusWindowView.as_view(),
        name="status_window",
    ),
    path(
        "works_done_today/<int:telegram_id>/",
        WorksDoneToday.as_view(),
        name="works_done_today",
    ),
    path("operations/", OperationList.as_view(), name="operations"),
    path("workers_static_info/", WorkersStaticInfo.as_view(), name="workers_static_info"),
]
