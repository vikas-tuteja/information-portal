from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import JsonResponse

from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework import permissions

from myaccount.models import UserDetail
from myaccount.serializers import UserSerializer, AuthUserSerializer

# Create your views here.
class SignIn(generics.CreateAPIView):
    """
        sample payload
        {
          "username": "9821115535",
          "password": "9821115535"
        }
    """
    permission_classes = []
    serializer_class = AuthUserSerializer
    queryset = User.objects.none()
    
    def post(self, request, *args, **kwargs):
        kwargs.update(request.data)
        key = None
        status = False
        user = authenticate(
            username = kwargs.get('username', kwargs.get('mobile')),
            password = kwargs.get('password'))

        if not user:
            message = 'Error: Invalid credentials'
            user = type('User', (object,), {
                "first_name": str(), "last_name": str()})
        else:
            key = Token.objects.get(user=user).key
            status = True
            message = 'Successfully logged in'

        return JsonResponse( data={
            'status':status,
            'message':message,
            'token': key,
            'name': '{} {}'.format(user.first_name, user.last_name)
        })


class SignUp(generics.CreateAPIView):
    """
        sample payload
        {
          "first_name": "U",
          "last_name": "B",
          "mobile": "9821115535",
          "password": "9821115535",
          "confirm_password": "9821115535",
          "email": "vikastuteja21@gmail.com"
        }
    """
    permission_classes = []
    serializer_class = UserSerializer
    queryset = UserDetail.objects.all()

    def post(self, request, *args, **kwargs):
        kwargs.update(request.data)
        
        # check if user already exists
        username = kwargs.get('username', kwargs.get('mobile'))
        email = kwargs.get('email')
        password = kwargs.get('password')
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        exists = UserDetail.objects.filter(
            Q(auth_user__username=username) | Q(mobile=username))

        if exists:
            key = None
            status = False
            message = 'User with this email or mobile already exists '
        else:
            try:
                # create auth user first
                auth_user = User.objects.create(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                )
                auth_user.set_password(kwargs.get('password', kwargs.get('mobile')))
                auth_user.save()
                
                # then create userdetails
                user_detail = UserDetail.objects.create(
                    auth_user = auth_user,
                    mobile = username,
                )
                user_detail.save()

                # then create auth token
                token = Token.objects.create(user=auth_user)
            
                # automatic login after registration
                user = authenticate(
                    username = username,
                    password = password
                )
                # this is not required
                # auth_login(request, user)

                key = token.key
                status = True
                message = 'User created successfully.'

                # TODO: welcome email
                """email_data = econf.get(user_role)['welcome']
                html_content = email_data['html'] % {'username': username, 'password': password}

                emailobj = SendMail()
                emailobj.set_params(
                        recipient_list=username, 
                        subject=email_data['subject'],
                        text_content=email_data['plain_text'],
                        html_content=html_content,
                )
                emailobj.send_mail()"""
            except:
                pass
        return JsonResponse( data={
            'status':status,
            'message':message,
            'token': key,
            'name': '{} {}'.format(first_name, last_name)
        })

class ChangePassword(generics.CreateAPIView):
    """
    changing the password to a new password
    METHOD : PUT
    {
      "username": "9821115535",
      "password": "9821115535",
      "new_password": "qwerty123"
      "confirm_new_password": "qwerty123"
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = UserDetail.objects.none()
    lookup_field = "auth_user__username"
    lookup_url_kwarg = "user_email"
    allowed_methods = ['PUT',]

    def put(self, request, *args, **kwargs):
        status = False
        kwargs.update(request.data)
        auth_user = authenticate(
            username = kwargs.get('username'),
            password = kwargs.get('password')
        )

        if not getattr(auth_user, 'username', None):
            message = 'Error: Old Password is incorrect'
        else:
            auth_user.set_password(kwargs.get('new_password'))
            auth_user.save()
            status, message = True, 'Password changed Successfully'

            # make user login again with new credentials
            auth_user = authenticate( 
                username = kwargs.get('username'),
                password = kwargs.get('new_password')
            )
            auth_login(request, auth_user)

        return JsonResponse(data={
            'status':status,
            'message':message
        })


class ForgotPassword(generics.CreateAPIView):
    """
    this will change the password of the user to 
    his/her 10 digit mobile number
    METHOD : PUT
    POST PARAMS: username
    {
     "username": "9560012945"
    }

    """
    permission_classes = []
    serializer_class = UserSerializer
    queryset = UserDetail.objects.all()
    allowed_methods = ['PUT',]

    def put(self, request, *args, **kwargs):
        status = False
        username = request.data.get('username')
        if not username:
            message = 'Error: Please enter username.'

        else:
            try:
                userObj = UserDetail.objects.get(auth_user__username=username)
                if not userObj:
                    message = 'Error: %s user not found.' % username
                else:
                    userObj.auth_user.set_password( str(username)[-10:] )
                    userObj.auth_user.save()
                    status = True
                    message = 'Your new password is reset to your 10 digit mobile number.'
            except UserDetail.DoesNotExist:
                    message = 'User with this mobile does not exists. Please register first.'

        return JsonResponse(data={
            'status':status,
            'message':message
        })

class Logout(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AuthUserSerializer
    queryset = User.objects.none()

    def get(self, request, *args, **kwargs):
        auth_logout(request)

        return JsonResponse(data={
            'status': True,
            'message': 'Logged out successfully' 
        })


class UserDetailUpdate( generics.UpdateAPIView ):
    """
        update payload:
        {
          "first_name": "Viki"
          "last_name": "Dudes"
        }
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    allowed_methods = ['PUT',]

    def get_queryset(self):
        return UserDetail.objects.get(auth_user=self.request.user)
 
    def get_object(self):
        qs = self.filter_queryset(self.get_queryset())
        return qs

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.auth_user.first_name = request.data['first_name']
        obj.auth_user.last_name = request.data['last_name']
        obj.auth_user.save()
        return JsonResponse( data={
            'message': 'User Updated' ,
            'status': True,
        })

class UserDetailListing( generics.ListAPIView ):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserDetail.objects.filter(auth_user=self.request.user)
