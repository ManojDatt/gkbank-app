from django.urls import path
from .views import DownloadBankStatement

urlpatterns = [
	path('download-statement', DownloadBankStatement.as_view(), name="download_statement"),
]