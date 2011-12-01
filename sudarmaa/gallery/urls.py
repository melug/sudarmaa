from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from gallery.views import ImageList, UploadImage

urlpatterns = patterns("", 
    url(r"^gallery/choose/$", login_required(ImageList.as_view()),
    name="choose-image"),
    url(r"^gallery/upload/$", login_required(UploadImage.as_view()),
    name="upload-image"),
)

