from rest_framework import authentication
from rest_framework.authtoken.models import Token

KEYWORD = 'Bearer'


class BearerAuthentication(authentication.TokenAuthentication):
    '''
    Simple token based authentication using utvsapitoken.
    Clients should authenticate by passing the token key in the 'Authorization'
    HTTP header, prepended with the string 'Bearer '.  For example:
    Authorization: Bearer 956e252a-513c-48c5-92dd-bfddc364e812
    '''
    keyword = KEYWORD

def get_token(user):
    token = Token.objects.get(user=user).key
    return '{} {}'.format(KEYWORD, token)
