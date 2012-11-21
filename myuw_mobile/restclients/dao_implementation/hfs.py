from os.path import dirname
from restclients.dao_implementation.mock import get_mockdata_url
from restclients.dao_implementation.live import get_con_pool, get_live_url
import logging
from myuw_mobile.logger.logback import log_info

class File(object):
    """
    This implementation returns mock/static content.  
    Use this DAO with this configuration:

    RESTCLIENTS_HFS_DAO_CLASS = 'myuw_mobile.restclients.dao_implementation.hfs.File'
    """
    def getURL(self, url, headers):
        """
        Return the url for accessing the mock data in local file
        :param url:
            in the format of "hfs/servlet/hfservices?sn=<student number>"
        """
        return get_mockdata_url("hfs", "file", url, headers,
                                dir_base=dirname(__file__))

class Live(object):
    """
    This DAO provides real data.
    Access is restricted to localhost.
    """
    logger = logging.getLogger('myuw_mobile.restclients.dao_implementation.hfs.Live')
    pool = None

    def getURL(self, url, headers):
        """
        Return the absolute url for accessing live data
        :param url:
            in the format of "hfs/servlet/hfservices?sn=<student number>"
        """
        host = 'http://localhost:80/'
        if Live.pool is None:
            Live.pool = get_con_pool(host, None, None,
                                     socket_timeout=5.0,
                                     max_pool_size=5)
        log_info(Live.logger, Live.pool)
        return get_live_url (Live.pool, 'GET',
                             host, url, headers=headers)
