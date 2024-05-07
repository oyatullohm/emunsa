def deco_login(fun):
    def wrapper(request,pk=None,*args,**kwargs):
        if request.user.is_authenticated  :
            return fun(self, request, pk,*args, **kwargs)
        return redirect('main:login')
    return wrapper