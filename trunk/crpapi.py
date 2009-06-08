""" 
	Python library for interacting with the CRP API.

    The CRP API (http://www.opensecrets.org/action/api_doc.php) provides campaign 
	finance and other data from the Center for Responsive Politics.

	See README.rst for methods and usage
"""

__author__ = "James Turk (jturk@sunlightfoundation.com)"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2009 Sunlight Labs"
__license__ = "BSD"

import urllib, urllib2
try:
    import json
except ImportError:
    import simplejson as json

class CRPApiError(Exception):
    """ Exception for CRP API errors """

# results #
class CRPApiObject(object):
    def __init__(self, d):
        self.__dict__ = d

class Contributor(CRPApiObject):
    def __str__(self):
        return '%s %s' % (self.org_name,self.total)

class Industry(CRPApiObject):
    def __str__(self):
        return '%s %s' % (self.industry_name,self.total)

class Sector(CRPApiObject):
    def __str__(self):
        return '%s %s' % (self.sector_name,self.total)

class Trip(CRPApiObject):
    def __str__(self):
        return '%s %s' % (self.traveler,self.destination)

# namespaces #

class CRP(object):

    apikey = None

    @staticmethod
    def _apicall(func, params):
        if CRP.apikey is None:
            raise CRPApiError('Missing CRP apikey')

        url = 'http://api.opensecrets.org/?method=%s&output=json&apikey=%s&%s' % \
              (func, CRP.apikey, urllib.urlencode(params))
        try:
            response = urllib2.urlopen(url).read()
            return json.loads(response)['response']
        except urllib2.HTTPError, e:
            raise CRPApiError(e.read())
        except (ValueError, KeyError), e:
            raise CRPApiError('Invalid Response')

    class candSummary(object):
        @staticmethod
        def get(**kwargs):
            result = CRP._apicall('candSummary', kwargs)['summary']
            return result['@attributes']

    class candContrib(object):
        @staticmethod
        def get(**kwargs):
            results = CRP._apicall('candContrib', kwargs)['contributors']['contributor']
            return [Contributor(l['@attributes']) for l in results]

    class candIndustry(object):
        @staticmethod
        def get(**kwargs):
            results = CRP._apicall('candIndustry', kwargs)['industries']['industry']
            return [Industry(l['@attributes']) for l in results]

    class candSector(object):
        @staticmethod
        def get(**kwargs):
            results = CRP._apicall('candSector', kwargs)['sectors']['sector']
            return [Sector(l['@attributes']) for l in results]

    class candIndByInd(object):
        @staticmethod
        def get(**kwargs):
            result = CRP._apicall('CandIndByInd', kwargs)['candIndus']
            return result['@attributes']

    class memTravelTrips(object):
        @staticmethod
        def get(**kwargs):
            results = CRP._apicall('memTravelTrips', kwargs)['trips']['trip']
            return [Trip(l['@attributes']) for l in results]