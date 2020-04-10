from django.urls import resolve



def SSLHoursMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        print('namespace:name (to add to STRONGHOLD_PUBLIC_NAMED_URLS) ', resolve(request.path_info).view_name)


        return response

    return middleware


