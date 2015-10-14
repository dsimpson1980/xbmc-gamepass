import os

from resources.lib import yql
from resources.lib.yql.storage import FileTokenStore
import config
import xbmc

cache_dir = os.path.join(xbmc.translatePath(
    'special://userdata'), 'addon_data', 'plugin.video.nfl.gamepass')

def get_y3():
    """Return an oauth connection from yql using consumer_key and
    consumer_secret that is either cached or requested from the user

    Parameters
    ----------
    None

    Returns
    -------
    yql.ThreeLegged
    """
    consumer_key, consumer_secret = config.get_consumer_secret()
    y3 = yql.ThreeLegged(consumer_key, consumer_secret,
                         disable_ssl_certificate_validation=True)
    return y3

def get_token(y3, dialog=None, _cache_dir=None):
    """Check if there is a cached token and if so retrieve it else ask the user
    for a new token using dialog.

    Parameters
    ----------
    y3: yql.ThreeLegged
        yql connection to use to query data
    dialog: function
        A dialog function that will interact with the user and return verifier

    Returns
    -------
    yql.YahooToken
        Either the cached token or a newly requested token
    """
    if _cache_dir is None:
        _cache_dir = cache_dir
    if not os.access(_cache_dir, os.R_OK):
        os.mkdir(_cache_dir)
    token_store = FileTokenStore(_cache_dir, secret='sasfasdfdasfdaf')
    stored_token = token_store.get('foo')
    if not stored_token:
        request_token, auth_url = y3.get_token_and_auth_url()
        if dialog is not None:
            verifier = dialog(auth_url)
        else:
            print "Visit url %s and get a verifier string" % auth_url
            verifier = raw_input("Enter the code: ")
        token = y3.get_access_token(request_token, verifier)
        token_store.set('foo', token)
    else:
        token = y3.check_token(stored_token)
        if token != stored_token:
            token_store.set('foo', token)
    return token

def get_matchup_points(y3, token, league_key):
    """Extract points and projected points from each of the matchups in
     fantasysports.leagues.scoreboard

    Parameters
    ----------
    y3: yql.ThreeLegged
        The active connection for yql queries
    token: yql.YahooToken
        The token used for the y3 connection
    league_key: str
        The league key in the form XXX.l.XXXX

    Returns
    -------
    list(list(dict))
        A list with length the number of matchups in the league = num_teams /2
        Each sublist is the first and second team.  Each dict is the team name,
        points, and projected_points
    """
    query = """SELECT *
                 FROM fantasysports.leagues.scoreboard
                WHERE league_key = '%s'""" % league_key
    data_yql = y3.execute(query, token=token).rows[0]
    matchups = data_yql['scoreboard']['matchups']['matchup']

    def extract_matchup(team):
        """Extract dict consisting of team name, points and projected points

        Parameters
        ----------
        team: dict
            The team dict extracted from matchup in yahoo

        Returns
        -------
        dict:
            dict of name, points, and projected_points
        """
        result = dict(name=team['name'])
        result['points'] = float(team['team_points']['total'])
        result['projected_points'] = float(team['team_projected_points']['total'])
        return result
    matchups = [[extract_matchup(t) for t in m['teams']['team']] for m in matchups]
    return matchups
