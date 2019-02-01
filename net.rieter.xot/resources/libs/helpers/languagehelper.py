#===============================================================================
# LICENSE Retrospect-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/
# or send a letter to Creative Commons, 171 Second Street, Suite 300,
# San Francisco, California 94105, USA.
#===============================================================================

from addonsettings import AddonSettings


class LanguageHelper:
    UnknownId = 1
    AllFavouritesId = 30500
    FavouriteId = 30501
    FavouritesId = 30502
    ChannelFavourites = 30503
    HideId = 30505
    ChannelsId = 30507
    NoFavsId = 30508
    NoPlaybackId = 30509
    NewVersionId = 30516
    NewVersion2Id = 30517
    RepoWarningId = 30520
    RepoWarningDetailId = 30521
    ChannelMessageId = 30522
    ErrorId = 30523
    NoVideosId = 30524
    NoStreamsId = 30525
    ProxyChangeConfirmTitle = 30038
    ProxyChangeConfirm = 30039
    AddOnSettingsId = 30528
    RefreshListId = 30529
    CheckUpdatesId = 30530
    BitrateSelection = 30020

    ChannelSelection = 30507
    # InitializingId = 30531
    # ImportCommonId = 30532
    # DeterminSkinId = 30533
    # CheckForUpdatesId = 30534
    # RepoVerificationId = 30535
    # CacheCheckId = 30536

    Page = 30537
    NoLiveStreamId = 30538
    LiveStreamTitleId = 30539
    GeoLockedId = 30540
    PremiumPaid = 30049
    DrmProtected = 30050
    HiddenItem = 30051
    QueueItemId = 30541
    StartingAddonId = 30542
    SeasonId = 30543
    EpisodeId = 30544
    StartWith = 30545
    OtherChars = 30546
    MorePages = 30547
    Clips = 30548
    ErrorList = 30549
    ErrorNoEpisodes = 30550
    DrmTitle = 30554
    DrmText = 30555
    PaidTitle = 30560
    PaidText = 30561
    MissingCredentials = 30562
    CloakItem = 30563
    UnCloakItem = 30564
    CloakFirstTime = 30565
    CloakMessage = 30566
    AddonsNotEnabledTitle = 30567
    AddonsNotEnabledText = 30568

    Active = 30068
    ShowChannelSettings = 30069
    InitChannelTitle = 30556
    InitChannelText = 30557
    FetchTexturesTitle = 30558
    FetchTexturesText = 30559

    VaultNewPin = 30590
    VaultNoPin = 30591
    VaultRepeatPin = 30592
    VaultPinsDontMatch = 30593
    VaultSpecifySetting = 30594
    VaultInputPin = 30595
    VaultIncorrectPin = 30596
    VaultResetConfirm = 30597
    VaultReset = 30092

    LogPostSetting = 30598
    LogPostLogUrl = 30599
    LogPostSuccessTitle = 30600
    LogPostError = 30601
    LogPostErrorTitle = 30602

    Today = 30551
    Yesterday = 30552
    DayBeforeYesterday = 30553

    __Categories = {"None": 30100,
                    "Regional": 30101,
                    "National": 30102,
                    "Video": 30103,
                    "Radio": 30104,
                    "Sport": 30105,
                    "Kids": 30106,
                    "Tech": 30107,
                    "Other": 30108}

    __LanguageMapping = {None:      30025,
                         "be":      30406,
                         "de":      30409,
                         "ee":      30408,
                         "en-gb":   30407,
                         "lt":      30403,
                         "lv":      30404,
                         "nl":      30401,
                         "no":      30405,
                         "se":      30402,
                         "dk":      30410}

    def __init__(self):
        pass

    @staticmethod
    def get_localized_category(category_name):
        """ Translates the category name into the language that is used within Kodi.

        @param str category_name: name of the category to lookup

        @rtype: str
        @return: Returns the localized version of the category name

        """
        string_id = LanguageHelper.__Categories.get(category_name, None)
        if not string_id:
            return category_name

        return LanguageHelper.get_localized_string(string_id, False)

    @staticmethod
    def get_full_language(language_id):
        """ Converts a language short ID to a localized Full language name.

        @param str language_id: the sort ID for the language

        @rtype: str
        @return: The long language

        Eg: nl -> Dutch, se -> Swedish
        """
        return LanguageHelper.get_localized_string(
            LanguageHelper.__LanguageMapping.get(language_id,
                                                 LanguageHelper.__LanguageMapping[None]))

    @staticmethod
    def get_localized_string(string_id, split_on_pipes=True, replace_pipes=False):
        """ Returns a localized Add-on string using the defined string_id.

        @param int string_id:        The ID for the string
        @param bool split_on_pipes:  If true, | cause a split and a list will be returned.
        @param bool replace_pipes:   If true, | will be replaced by \n.

        @rtype: str|list[str]
        @return: localized Add-on string use the defined string_id.

        """

        value = AddonSettings.get_localized_string(string_id)
        if split_on_pipes and "|" in value:
            return value.split("|")
        elif replace_pipes and "|" in value:
            return value.replace("|", "\n")
        else:
            return value
