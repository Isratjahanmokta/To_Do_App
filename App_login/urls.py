from App_login import views
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = "App_login"

schema_view = get_schema_view(
   openapi.Info(
      title="Posts API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('task_list/', views.TaskList.as_view()),
    path('task_create/', views.TaskCreate.as_view()),
    path('task_detail/<id>', views.TaskDetail.as_view()),
    path('task_update/<id>', views.TaskUpdate.as_view()),
    path('task_delete/<id>', views.TaskDelete.as_view()),
    path('sign_up/', views.SignUp.as_view()),
    path('Log_out/', views.LogoutView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 ]