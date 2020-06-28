import graphene
from django.contrib.auth import get_user_model, authenticate, logout, login
from .mdtypes import UserType
import logging

class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    sessionid = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        try:
            print('[%s][%s][%s]' % (info.context.path, info.context.method, info.context.session.keys()))
            
            user = authenticate(username = email, password = password)

            if not user:
                raise Exception('Usuário ou senha inválida!')
            if (user.is_active):
                login(info.context, user)
                return LoginUser(user=user, sessionid=info.context.session.session_key)
            else:
                raise Exception('Usuário está inativo!')

        except Exception as e:
            raise Exception('Ops %s' %(e))
        

class LogoutUser(graphene.Mutation):
    logout = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        print('[%s][%s][%s]' % (info.context.path, info.context.method, info.context.user))

        user = info.context.user
        if user.is_anonymous:
            return cls(logout=False)

        logout(info.context)
        return cls(logout=True)


class AuthMutation(graphene.ObjectType):
    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()