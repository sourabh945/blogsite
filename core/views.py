from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index_page(request):
    return HttpResponseRedirect('/home/')