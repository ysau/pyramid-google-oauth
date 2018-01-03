# -*- coding: utf-8 -*-
# main.py

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from authomatic import Authomatic
from authomatic.adapters import WebObAdapter

from config import CONFIG

authomatic = Authomatic(config=CONFIG, secret='some random secret string')


def login(request):

    # We will need the response to pass it to the WebObAdapter.
    response = Response()

    # Get the internal provider name URL variable.
    provider_name = request.matchdict.get('provider_name')

    # Start the login procedure.
    result = authomatic.login(WebObAdapter(request, response), provider_name)

    # Do not write anything to the response if there is no result!
    if result:
        # If there is result, the login procedure is over and we can write to
        # response.
        response.write('<a href="..">Home</a>')

        if result.error:
            # Login procedure finished with an error.
            response.write(
                u'<h2>Damn that error: {0}</h2>'.format(result.error.message))

        elif result.user:
            # Hooray, we have the user!

            # OAuth 2.0 and OAuth 1.0a provide only limited user data on login,
            # We need to update the user to get more info.
            #if not (result.user.name and result.user.id):
            result.user.update()

            #print(result.user.profile)
            # Welcome the user.
            response.write(u'<h1>Hi {0}</h1>'.format(result.user.first_name))
            response.write(u'<h2>Your id is: {0}</h2>'.format(result.user.id))
            response.write(
                u'<h2>Your email is: {0}</h2>'.format(result.user.email))

            # Seems like we're done, but there's more we can do...

            # If there are credentials (only by AuthorizationProvider),
            # we can _access user's protected resources.
            if result.user.credentials:

                # Each provider has it's specific API.
                if result.provider.name == 'google':
                    response.write('Your are logged in with Google.<br />')

    # It won't work if you don't return the response
    return response


def home(request):
    return Response('''
        Login with <a href="login/google">Google</a>.<br />
    ''')


if __name__ == '__main__':
    config = Configurator()

    config.add_route('home', '/')
    config.add_view(home, route_name='home')

    config.add_route('login', '/login/{provider_name}')
    config.add_view(login, route_name='login')

    app = config.make_wsgi_app()
    server = make_server('127.0.0.1', 8080, app)
    server.serve_forever()
