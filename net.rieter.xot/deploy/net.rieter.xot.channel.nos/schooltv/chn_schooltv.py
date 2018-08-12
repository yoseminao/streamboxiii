import chn_class
import mediaitem

# from config import Config
from logger import Logger
from helpers.jsonhelper import JsonHelper
from urihandler import UriHandler
from streams.npostream import NpoStream
from helpers.languagehelper import LanguageHelper
from helpers.htmlentityhelper import HtmlEntityHelper
from helpers.datehelper import DateHelper


class Channel(chn_class.Channel):
    """
    main class from which all channels inherit
    """

    def __init__(self, channelInfo):
        """Initialisation of the class.

        Arguments:
        channelInfo: ChannelInfo - The channel info object to base this channel on.

        All class variables should be instantiated here and this method should not
        be overridden by any derived classes.

        """

        chn_class.Channel.__init__(self, channelInfo)

        # ============== Actual channel setup STARTS here and should be overwritten from derived classes ===============
        self.noImage = "schooltvimage.jpg"

        self.baseUrl = "http://apps-api.uitzendinggemist.nl"
        self.mainListUri = "http://m.schooltv.nl/api/v1/programmas.json"

        # mainlist stuff
        self._AddDataParser("http://m.schooltv.nl/api/v1/programmas.json", json=True,
                            name="All Shows (API v1)",
                            preprocessor=self.AddCategories,
                            parser=(), creator=self.CreateEpisodeItem)

        self._AddDataParser("http://m.schooltv.nl/api/v1/programmas/tips.json?size=100", json=True,
                            name="Tips (API v1)",
                            parser=(), creator=self.CreateEpisodeItem)

        self._AddDataParsers(["http://m.schooltv.nl/api/v1/programmas/",
                              "http://m.schooltv.nl/api/v1/categorieen/",
                              "http://m.schooltv.nl/api/v1/leeftijdscategorieen/"],
                             json=True,
                             name="Paged Video Items (API v1)",
                             preprocessor=self.AddPageItems,
                             parser=('results', ), creator=self.CreateVideoItem)

        self._AddDataParser("http://m.schooltv.nl/api/v1/categorieen.json?size=100", json=True,
                            name="Categories (API v1)",
                            parser=(), creator=self.CreateCategory)

        self._AddDataParser("http://m.schooltv.nl/api/v1/afleveringen/", json=True,
                            name="Video Updater (API v1)",
                            updater=self.UpdateVideoItem)

        # ===============================================================================================================
        # non standard items
        self.__PageSize = 100

        # ===============================================================================================================
        # Test cases:
        # schooltv-weekjournaal: paging
        # Aarde & Ruimte: -> has both ODI+MP4 and ODI+M3U8
        # Wiskunden tweede fase: fylosofie en waarheid - waaronaan... -> ODI+M3u8

        # ====================================== Actual channel setup STOPS here =======================================
        return

    def CreateEpisodeItem(self, resultSet):
        """Creates a new MediaItem for an episode

        Arguments:
        resultSet : list[string] - the resultSet of the self.episodeItemRegex

        Returns:
        A new MediaItem of type 'folder'

        This method creates a new MediaItem from the Regular Expression or Json
        results <resultSet>. The method should be implemented by derived classes
        and are specific to the channel.

        """

        Logger.Trace(resultSet)

        url = "http://m.schooltv.nl/api/v1/programmas/%s/afleveringen.json?size=%s&sort=Nieuwste" % (resultSet['mid'], self.__PageSize)
        item = mediaitem.MediaItem(resultSet['title'], url)
        item.thumb = resultSet.get('image', self.noImage)
        item.icon = self.icon

        item.description = resultSet.get('description', None)
        ageGroups = resultSet.get('ageGroups', ['Onbekend'])
        item.description = "%s\n\nLeeftijden: %s" % (item.description, ", ".join(ageGroups))
        return item

    def AddCategories(self, data):
        """ Add categories to the main listing

        @param data:    the Parsed Data
        @return:        a tuple of data and items
        """

        Logger.Info("Performing Pre-Processing")
        items = []

        cat = mediaitem.MediaItem("\b.: Categorie&euml;n :.",
                                  "http://m.schooltv.nl/api/v1/categorieen.json?size=100")
        cat.thumb = self.noImage
        cat.icon = self.icon
        cat.fanart = self.fanart
        cat.complete = True
        cat.dontGroup = True
        items.append(cat)

        tips = mediaitem.MediaItem("\b.: Tips :.",
                                   "http://m.schooltv.nl/api/v1/programmas/tips.json?size=100")
        tips.thumb = self.noImage
        tips.icon = self.icon
        tips.fanart = self.fanart
        tips.complete = True
        tips.dontGroup = True
        items.append(tips)

        data = JsonHelper(data)
        ages = mediaitem.MediaItem("\b.: Leeftijden :.", "")
        ages.thumb = self.noImage
        ages.icon = self.icon
        ages.fanart = self.fanart
        ages.complete = True
        ages.dontGroup = True
        for age in ("0-4", "5-6", "7-8", "9-12", "13-15", "16-18"):
            ageItem = mediaitem.MediaItem(
                "%s Jaar" % (age,),
                "http://m.schooltv.nl/api/v1/leeftijdscategorieen/%s/afleveringen.json?"
                "size=%s&sort=Nieuwste" % (age, self.__PageSize))
            ageItem.thumb = self.noImage
            ageItem.icon = self.icon
            ageItem.fanart = self.fanart
            ageItem.complete = True
            ageItem.dontGroup = True
            ages.items.append(ageItem)

            # We should list programs instead of videos, so just prefill them here.
            for program in data.GetValue():
                if age in program['ageGroups']:
                    ageItem.items.append(self.CreateEpisodeItem(program))
        items.append(ages)

        Logger.Debug("Pre-Processing finished")
        return data, items

    def CreateCategory(self, resultSet):
        """ Creates a Category Media Item

        @param resultSet:
        @return:
        """
        Logger.Trace(resultSet)

        title = HtmlEntityHelper.UrlEncode(resultSet['title'])
        url = "http://m.schooltv.nl/api/v1/categorieen/%s/afleveringen.json?sort=Nieuwste&age_filter=&size=%s" % (title, self.__PageSize)
        item = mediaitem.MediaItem(resultSet['title'], url)
        item.thumb = resultSet.get('image', self.noImage)
        item.description = "Totaal %(count)s videos" % resultSet
        item.icon = self.icon
        return item

    def AddPageItems(self, data):
        """ Adds page items to the main listing

        @param data:    the Parsed Data
        @return:        a tuple of data and items
        """

        Logger.Info("Performing Pre-Processing")
        items = []
        json = JsonHelper(data)
        totalResults = json.GetValue("totalResults")
        fromValue = json.GetValue("from")
        sizeValue = json.GetValue("size")

        if fromValue + sizeValue < totalResults:
            morePages = LanguageHelper.GetLocalizedString(LanguageHelper.MorePages)
            url = self.parentItem.url.split('?')[0]
            url = "%s?size=%s&from=%s&sort=Nieuwste" % (url, sizeValue, fromValue+sizeValue)
            Logger.Debug("Adding next-page item from %s to %s", fromValue+sizeValue, fromValue+sizeValue+sizeValue)

            nextPage = mediaitem.MediaItem(morePages, url)
            nextPage.icon = self.parentItem.icon
            nextPage.fanart = self.parentItem.fanart
            nextPage.thumb = self.parentItem.thumb
            nextPage.dontGroup = True
            items.append(nextPage)

        Logger.Debug("Pre-Processing finished")
        return json, items

    def CreateVideoItem(self, resultSet):
        """Creates a MediaItem of type 'video' using the resultSet from the regex.

        Arguments:
        resultSet : tuple (string) - the resultSet of the self.videoItemRegex

        Returns:
        A new MediaItem of type 'video' or 'audio' (despite the method's name)

        This method creates a new MediaItem from the Regular Expression or Json
        results <resultSet>. The method should be implemented by derived classes
        and are specific to the channel.

        If the item is completely processed an no further data needs to be fetched
        the self.complete property should be set to True. If not set to True, the
        self.UpdateVideoItem method is called if the item is focussed or selected
        for playback.

        """

        Logger.Trace(resultSet)

        title = resultSet["title"]
        if title is None:
            Logger.Warning("Found item with all <null> items. Skipping")
            return None

        if "subtitle" in resultSet and resultSet['subtitle'].lower() not in title.lower():
            title = "%(title)s - %(subtitle)s" % resultSet

        url = "http://m.schooltv.nl/api/v1/afleveringen/%(mid)s.json" % resultSet
        item = mediaitem.MediaItem(title, url)
        item.description = resultSet.get("description", "")
        ageGroups = resultSet.get('ageGroups', ['Onbekend'])
        item.description = "%s\n\nLeeftijden: %s" % (item.description, ", ".join(ageGroups))

        item.thumb = resultSet.get("image", "")
        item.icon = self.icon
        item.type = 'video'
        item.fanart = self.fanart
        item.complete = False
        item.SetInfoLabel("duration", resultSet['duration'])

        if "publicationDate" in resultSet:
            broadcastDate = DateHelper.GetDateFromPosix(int(resultSet['publicationDate']))
            item.SetDate(broadcastDate.year,
                         broadcastDate.month,
                         broadcastDate.day,
                         broadcastDate.hour,
                         broadcastDate.minute,
                         broadcastDate.second)
        return item

    def UpdateVideoItem(self, item):
        Logger.Debug('Starting UpdateVideoItem for %s (%s)', item.name, self.channelName)

        data = UriHandler.Open(item.url, proxy=self.proxy, additionalHeaders=item.HttpHeaders)
        json = JsonHelper(data)

        part = item.CreateNewEmptyMediaPart()
        part.Subtitle = NpoStream.GetSubtitle(json.GetValue("mid"), proxy=self.proxy)

        for stream in json.GetValue("videoStreams"):
            if not stream["url"].startswith("odi"):
                part.AppendMediaStream(stream["url"], stream["bitrate"]/1000)
                item.complete = True

        if item.HasMediaItemParts():
            return item

        for s, b in NpoStream.GetStreamsFromNpo(None, json.GetValue("mid"), proxy=self.proxy):
            item.complete = True
            part.AppendMediaStream(s, b)

        return item
