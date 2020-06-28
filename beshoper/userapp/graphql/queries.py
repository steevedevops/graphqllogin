import graphene
from .mdtypes import UserType
from beshoper.decorator.decorators import user_passes_test, group_seller_required


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserType)
    
    @group_seller_required
    def resolve_user(self, info, **kwargs):
        return info.context.user
        