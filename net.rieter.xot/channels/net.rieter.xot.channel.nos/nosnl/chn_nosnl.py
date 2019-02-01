import mediaitem
import chn_class
import time
import base64

from helpers.jsonhelper import JsonHelper
from helpers.encodinghelper import EncodingHelper
from helpers.datehelper import DateHelper
from helpers.languagehelper import LanguageHelper

from logger import Logger
from streams.m3u8 import M3u8
from urihandler import UriHandler


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
        self.noImage = "nosnlimage.png"

        # setup the urls
        # self.mainListUri = "http://nos.nl/"
        self.mainListUri = "#getcategories"

        # we need specific headers: APK:NosHttpClientHelper.java
        salt = int(time.time())
        # key = "%sRM%%j%%l@g@w_A%%" % (salt,)
        # Logger.Trace("Found Salt: %s and Key: %s", salt, key)
        # key = EncodingHelper.encode_md5(key, toUpper=False)
        # self.httpHeaders = {"X-NOS-App": "Google/x86;Android/4.4.4;nl.nos.app/3.1",
        #                     "X-NOS-Salt": salt,
        #                     "X-NOS-Key": key}

        userAgent = "%s;%d;%s/%s;Android/%s;nl.nos.app/%s" % ("nos", salt, "Google", "Nexus", "6.0", "5.1.1")
        string = ";UB}7Gaji==JPHtjX3@c%s" % (userAgent, )
        string = EncodingHelper.encode_md5(string, to_upper=False).zfill(32)
        xnos = string + base64.b64encode(userAgent)
        self.httpHeaders = {"X-Nos": xnos}

        self.baseUrl = "http://nos.nl"

        # setup the main parsing data
        self._add_data_parser(self.mainListUri, preprocessor=self.GetCategories)
        self._add_data_parser("*",
                              # No longer used: preprocessor=self.AddNextPage,
                              json=True,
                              parser=['items', ],
                              creator=self.CreateJsonVideo, updater=self.UpdateJsonVideo)
        self._add_data_parser("*",
                              json=True,
                              parser=['links',],
                              creator=self.create_page_item)

        #===============================================================================================================
        # non standard items
        # self.__IgnoreCookieLaw()
        self.__pageSize = 50

        # ====================================== Actual channel setup STOPS here =======================================
        return

    def GetCategories(self, data):
        """Performs pre-process actions for data processing

        Arguments:
        data : string - the retrieve data that was loaded for the current item and URL.

        Returns:
        A tuple of the data and a list of MediaItems that were generated.


        Accepts an data from the process_folder_list method, BEFORE the items are
        processed. Allows setting of parameters (like title etc) for the channel.
        Inside this method the <data> could be changed and additional items can
        be created.

        The return values should always be instantiated in at least ("", []).

        """

        Logger.info("Creating categories")
        items = []

        cats = {
            "Meest Bekeken": "https://api.nos.nl/mobile/videos/most-viewed/phone.json",
            "Nieuws": "https://api.nos.nl/nosapp/v3/items?mainCategories=nieuws&types=video&limit={0}".format(self.__pageSize),
            "Sport": "https://api.nos.nl/nosapp/v3/items?mainCategories=sport&types=video&limit={0}".format(self.__pageSize),
            "Alles": "https://api.nos.nl/nosapp/v3/items?types=video&limit={0}".format(self.__pageSize),
        }

        for cat in cats:
            item = mediaitem.MediaItem(cat, cats[cat])
            item.thumb = self.noImage
            item.icon = self.icon
            item.complete = True
            items.append(item)

        Logger.debug("Creating categories finished")
        return data, items

    def create_page_item(self, resultSet):
        items = []
        if 'next' in resultSet:
            title = LanguageHelper.get_localized_string(LanguageHelper.MorePages)
            url = resultSet['next']
            item = mediaitem.MediaItem(title, url)
            item.fanart = self.parentItem.fanart
            item.thumb = self.parentItem.thumb
            items.append(item)

        return items

    def CreateJsonVideo(self, resultSet):
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
        self.update_video_item method is called if the item is focussed or selected
        for playback.

        """

        videoId = resultSet['id']
        # category = resultSet["maincategory"].title()
        # subcategory = resultSet["subcategory"].title()

        url = "https://api.nos.nl/mobile/video/%s/phone.json" % (videoId, )
        item = mediaitem.MediaItem(resultSet['title'], url, type="video")
        item.icon = self.icon
        if 'image' in resultSet:
            images = resultSet['image']["formats"]
            matchedImage = images[-1]
            for image in images:
                if image["width"] >= 720:
                    matchedImage = image
                    break
            item.thumb = matchedImage["url"].values()[0]

        item.description = resultSet["description"]
        item.complete = False
        item.isGeoLocked = resultSet.get("geoprotection", False)

        # set the date and time
        date = resultSet["published_at"]
        timeStamp = DateHelper.get_date_from_string(date, date_format="%Y-%m-%dT%H:%M:%S+{0}".format(date[-4:]))
        item.set_date(*timeStamp[0:6])
        return item

    def UpdateJsonVideo(self, item):
        """Updates an existing MediaItem with more data.

        Arguments:
        item : MediaItem - the MediaItem that needs to be updated

        Returns:
        The original item with more data added to it's properties.

        Used to update none complete MediaItems (self.complete = False). This
        could include opening the item's URL to fetch more data and then process that
        data or retrieve it's real media-URL.

        The method should at least:
        * cache the thumbnail to disk (use self.noImage if no thumb is available).
        * set at least one MediaItemPart with a single MediaStream.
        * set self.complete = True.

        if the returned item does not have a MediaItemPart then the self.complete flag
        will automatically be set back to False.

        """

        Logger.debug('Starting update_video_item: %s', item.name)

        data = UriHandler.open(item.url, proxy=self.proxy, additional_headers=self.httpHeaders)
        jsonData = JsonHelper(data)
        streams = jsonData.get_value("formats")
        if not streams:
            return item

        qualities = {"720p": 1600, "480p": 1200, "360p": 500, "other": 0}  # , "http-hls": 1500, "3gp-mob01": 300, "flv-web01": 500}
        part = item.create_new_empty_media_part()
        urls = []
        for stream in streams:
            url = stream["url"].values()[-1]
            if url in urls:
                # duplicate url, ignore
                continue

            urls.append(url)

            # actually process the url
            if not url.endswith(".m3u8"):
                part.append_media_stream(
                    url=url,
                    bitrate=qualities.get(stream.get("name", "other"), 0)
                )
                item.complete = True
            # elif AddonSettings.use_adaptive_stream_add_on():
            #     contentType, url = UriHandler.header(url, self.proxy)
            #     stream = part.append_media_stream(url, 0)
            #     M3u8.SetInputStreamAddonInput(stream, self.proxy)
            #     item.complete = True
            else:
                contentType, url = UriHandler.header(url, self.proxy)
                for s, b in M3u8.get_streams_from_m3u8(url, self.proxy):
                    item.complete = True
                    # s = self.get_verifiable_video_url(s)
                    part.append_media_stream(s, b)

        return item

    def __IgnoreCookieLaw(self):
        """ Accepts the cookies from UZG in order to have the site available """

        Logger.info("Setting the Cookie-Consent cookie for www.uitzendinggemist.nl")

        # a second cookie seems to be required
        UriHandler.set_cookie(name='npo_cc', value='tmp', domain='.nos.nl')
        return
