
from django.urls import path

from api import views as api_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('user/token/', api_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/register/', api_views.RegisterView.as_view()),
    path('user/profile/<user_id>/', api_views.ProfileView.as_view()),

    # Post Endpoints
    path('post/category/list/', api_views.CategoryListApiView.as_view()),
    path('post/category/posts/<category_slug>/', api_views.PostCategoryListApiView.as_view()),
    path('post/lists/', api_views.PostListApiView.as_view()),
    path('post/detail/<post_slug>', api_views.PostDetailApiView.as_view()),
    path('post/like-post/', api_views.LikePostApiView.as_view())
]
