from django.http import HttpRequest
from django.conf import settings
from myuw_mobile.models import User
import logging


class UserService:
    _user_data = {}
    _logger = logging.getLogger('myuw_mobile.user.UserService')

    def get_log_user_info(self):
        """
        Return a dictionary of user, accessed path, and client information for logging
        """
        #self._log_data['user'] = self._get_userid_for_log() 
        #########return self._log_data
    
    def _get_userid_for_log(self):
        """
        Return <actual user netid> acting_as: <override user netid> if
        the user is acting as someone else, otherwise <actual user netid>
        """
        override_userid = self.get_override_user()
        actual_userid = self.get_original_user()
        if override_userid:
            log_userid = actual_userid + ' acting_as: ' + override_userid
        else:
            log_userid = actual_userid
        return log_userid

    def _require_middleware(self):
        if not "initialized" in UserService._user_data:
            print "You need to have this line in your MIDDLEWARE_CLASSES:"
            print "'myuw_mobile.user.UserServiceMiddleware',"

            raise Exception("You need the UserServiceMiddleware")

    def get_user(self):
        self._require_middleware()

        override = self.get_override_user()
        if override and len(override) > 0:
            return override

        actual = self.get_original_user()
        if not actual or len(actual) == 0:
            return self._get_authenticated_user()
        return actual

    def get_original_user(self):
        if "original_user" in UserService._user_data:
            return UserService._user_data["original_user"]

    def get_override_user(self):
        if "override_user" in UserService._user_data:
            return UserService._user_data["override_user"]

    def set_user(self, user):
        UserService._user_data["original_user"] = user
        UserService._user_data["session"]["_us_user"] = user

    def set_override_user(self, override):
        UserService._user_data["override_user"] = override
        UserService._user_data["session"]["_us_override"] = override

    def clear_override(self):
        UserService._user_data["override_user"] = None
        UserService._user_data["session"]["_us_override"] = None

    # the get_user / get_original_user / get_override_user 
    # should all really be returning user models.  But, i don't want 
    # to be serializing that data for each request. So for now:
    def get_user_model(self):
        netid = self.get_user()
        in_db = User.objects.filter(uwnetid=netid)

        if len(in_db) > 0:
            return in_db[0]

        new = User()
        new.uwnetid = netid
        new.save()

        return new

class UserServiceMiddleware(object):
    def __init__(self):
        _logger = logging.getLogger('myuw_mobile.user.UserService')

    def process_request(self, request):
        UserService._user_data["initialized"] = True

        session = request.session
        UserService._user_data["session"] = session

        if not "_us_user" in session:
            user = self._get_authenticated_user()
            if user:
                UserService._user_data["original_user"] = user
        else:
            UserService._user_data["original_user"] = session["_us_user"]

        if "_us_override" in session:
            UserService._user_data["override_user"] = session["_us_override"]

    def process_response(self, request, response):
        UserService._user_data = {}
        return response

    def _get_authenticated_user(self):
        if settings.DEBUG:
            netid = 'javerage'
        else:
            netid = request.user.username

        if netid:
            self.set_user(netid)
            return netid

        return None


