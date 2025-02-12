from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignUpView, SignInView, LogoutView, LatencyView, \
    UserInfoView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("info/", UserInfoView.as_view(), name="user_info"),
    path("latency/", LatencyView.as_view(), name="latency"),
]
