from myuw_mobile.dao.pws import get_netid_of_current_user
from myuw_mobile.models import User


def get_user_model():
    user_netid = get_netid_of_current_user()

    user, created = User.objects.get_or_create(uwnetid=user_netid)

    return user
