from django.conf import settings

def custom_processors(request):
    ctx = {}
    ctx['base_url'] = settings.BASE_URL
    return ctx