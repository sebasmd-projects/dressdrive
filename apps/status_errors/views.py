from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

template_name = "errorsTemplate.html"


def handler400(request, exception, *args, **argv):
    status = 400
    return render(
        request,
        template_name,
        status=status,
        context={
            "exception": str(exception),
            "title": _("Error 400"),
            "error": _("Bad Request"),
            "status": status
        }
    )


def handler403(request, exception, *args, **argv):
    status = 403
    return render(
        request,
        template_name,
        status=status,
        context={
            "exception": str(exception),
            "title": _("Error 403"),
            "error": _("Forbidden Request"),
            "status": status
        }
    )


def handler404(request, exception, *args, **argv):
    status = 404
    return render(
        request,
        template_name,
        status=status,
        context={
            "exception": str(exception),
            "title": _("Error 404"),
            "error": _("Page not Found"),
            "status": status
        }
    )


def handler500(request, *args, **argv):
    status = 500
    return render(
        request,
        template_name,
        status=500,
        context={
            "title": _("Error 500"),
            "error": _("Server Error"),
            "status": status
        }
    )
