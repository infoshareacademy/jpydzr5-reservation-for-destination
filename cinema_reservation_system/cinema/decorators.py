from . import models

def set_vars(view_func):
    """
    funkcja napełnia context właściwymy danymi - dla wszystkich zalogowanych widoków
    """
    def _decorated(request, *args, **kwargs):
        kwargs['context'] = {}
        cinemas = models.Cinema.objects.all()
        kwargs['context']['cinemas'] = cinemas
        kwargs['context']['menu_positions'] = [
            {"name": "Cennik", "url": "cinema:price_list"},
            {"name": "Repertuar", "url": "cinema:repertoire"},
            {"name": "Koszyk", "url": "cinema:basket"}
        ]

        if 'cinema' in request.session:
            kwargs['context']['selected_cinema'] = cinemas.filter(pk=request.session.get('cinema')).first()

        return view_func(request, *args, **kwargs)

    return _decorated
