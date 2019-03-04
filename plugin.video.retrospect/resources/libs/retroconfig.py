import os
import xml.dom.minidom

import xbmc

from version import Version


class Config:
    """Class with all the configuration constants"""

    def __init__(self):
        pass

    try:
        import xbmcaddon
        # calling xbmcaddon.Addon() only works on newer XBMC's. Should see if it keeps working
        # if not, then the addonId should be hard coded here.
        __addon = xbmcaddon.Addon()
        __path = __addon.getAddonInfo('path')
        __addon = None  # : Free up the static variable to make sure it is garbage collected
        pathDetection = "addon.getAddonInfo('path')"
    except:
        xbmc.log("Retrospect: using os.getcwd()", xbmc.LOGWARNING)
        __path = os.getcwd()
        pathDetection = "os.getcwd()"

    # the Kodi libs return unicode info, so we need to convert this
    #noinspection PyArgumentEqualDefault
    __path = __path.decode('utf-8')

    # get rootDir, addonsDir and profileDir
    rootDir = __path.replace(";", "")                        # : The root directory where Retrospect resides.
    addonDir = os.path.split(rootDir)[-1]                    # : The add-on directory of Kodi.
    rootDir = os.path.join(rootDir, '')                      # : The root directory where Retrospect resides.

    # determine the profile directory, where user data is stored.
    if xbmc.getCondVisibility("system.platform.xbox"):
        profileDir = os.path.join(xbmc.translatePath("special://profile/script_data/"), addonDir)
        profileUri = os.path.join("special://profile/script_data/", addonDir)
    else:
        profileDir = os.path.join(xbmc.translatePath("special://profile/addon_data/"), addonDir)
        profileUri = os.path.join("special://profile/addon_data/", addonDir)

    # the XBMC libs return unicode info, so we need to convert this
    #noinspection PyArgumentEqualDefault
    profileDir = profileDir.decode('utf-8')
    profileUri = profileUri.decode('utf-8')

    cacheDir = os.path.join(profileDir, 'cache', '')         # : The cache directory.
    favouriteDir = os.path.join(profileDir, 'favourites')    # : The favourites directory

    appName = "Retrospect"                                   # : Name of the XOT application (could be overwritten from the addon.xml)
    cacheValidTime = 7 * 24 * 3600                           # : Time the cache files are valid in seconds.

    logLevel = 10                                            # : Minimum log level that is being logged. (from logger.py) Defaults to Debug
    logFileNameAddon = "retrospect.log"                      # : Filename of the log file of the plugin

    googleAnalyticsId = "UA-3902785-11"                      # : Google Analytics ID for statistics

    # must be single quotes for build script
    __addonXmlPath = os.path.join(rootDir, 'addon.xml')
    __addonXmlcontents = xml.dom.minidom.parse(__addonXmlPath)
    for addonentry in __addonXmlcontents.getElementsByTagName("addon"):
        addonId = str(addonentry.getAttribute("id"))          # : The ID the addon has in Kodi (from addon.xml)
        __version = addonentry.getAttribute("version")        # : The Version of the addon (from addon.xml) in text
        version = Version(version=__version)                  # : The Version of the addon (from addon.xml)
        #noinspection PyRedeclaration
        appName = str(addonentry.getAttribute("name"))        # : The name from the addon (from addon.xml)

    updateUrl = "https://api.bitbucket.org/2.0/repositories/basrieter/xbmc-online-tv/downloads/"

    textureMode = "Cached"                                    # : The mode for the textures: Local, Remote or Cached
    textureUrl = \
        "https://cdn.rieter.net/plugin.video.retrospect.cdn"  # : The URL for the remote texture location

    logSenderApi = "1786d25d01392d572659bba76f95174f"         # : The Retrospect logsender API (Google Shortner API or PasteBinAPI)
