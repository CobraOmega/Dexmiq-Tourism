from django.shortcuts import get_object_or_404, render
from .serializers import PackagesSerializer
from rest_framework import viewsets
from .models import Packages

class PackagesViewSet(viewsets.ModelViewSet):
    queryset = Packages.objects.all()
    serializer_class = PackagesSerializer

def homepage(request):
    packages = Packages.objects.all()
    print(f"Number of packages found: {packages.count()}")
    return render(request, 'index.html', {'packages': packages})

def home_view(request):
       active_packages = Packages.objects.filter(is_active=True)
       return render(request, 'home.html', {'packages': active_packages})

def package_detail(request, id):
    package = get_object_or_404(Packages, id=id)
    return render(request, 'package_detail.html', {'package': package})
