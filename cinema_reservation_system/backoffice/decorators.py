from cinema import models


def set_vars(view_func):
    """
    funkcja napełnia context właściwymi danymi - dla wszystkich zalogowanych widoków
    """
    def _decorated(request, *args, **kwargs):
        kwargs['context'] = {}
        cinemas = models.Cinema.objects.all()
        kwargs['context']['cinemas'] = cinemas

        if 'selected_cinema_id' in request.session:
            kwargs['context']['selected_cinema'] = cinemas.filter(pk=request.session.get('selected_cinema_id')).first()
        return view_func(request, *args, **kwargs)

    return _decorated