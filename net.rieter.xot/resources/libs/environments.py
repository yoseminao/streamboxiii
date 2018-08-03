#===============================================================================
# LICENSE Retrospect-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/
# or send a letter to Creative Commons, 171 Second Street, Suite 300,
# San Francisco, California 94105, USA.
#===============================================================================


# noinspection PyClassHasNoInit
class Environments:

    """Enum class that holds the environments"""

    NoPlatform = 0
    Unknown = 1
    Xbox = 2
    Linux = 4
    Windows = 8
    OSX = 16
    ATV2 = 32
    IOS = 64
    Android = 128
    TVOS = 256          # such as ATV4

    # special groups
    Apple = OSX | ATV2 | IOS | TVOS
    Google = Android
    All = Xbox | Linux | Windows | OSX | ATV2 | IOS | Android | TVOS

    @staticmethod
    def Name(environment):
        """Returns a string representation of the Environments

        Arguments:
        environment : integer - The integer matching one of the
                                environments enums.

        Returns a string
        """

        if environment == Environments.OSX:
            return "OS X"
        elif environment == Environments.Windows:
            return "Windows"
        elif environment == Environments.Xbox:
            return "Xbox"
        elif environment == Environments.Linux:
            return "Linux"
        elif environment == Environments.IOS:
            return "iOS"
        elif environment == Environments.ATV2:
            return "Apple TV2"
        elif environment == Environments.TVOS:
            return "Apple TV OS"
        elif environment == Environments.Android:
            return "Android"
        elif environment == Environments.NoPlatform:
            return "No Platform"
        elif environment == Environments.Apple:
            return "Apple Device"
        else:
            return "Unknown"


if __name__ == "__main__":
    printFormat = "%-10s - %s"
    print printFormat % ("NoPlatform", Environments.Name(Environments.NoPlatform))
    print printFormat % ("Unknown", Environments.Name(Environments.Unknown))
    print printFormat % ("Xbox", Environments.Name(Environments.Xbox))
    print printFormat % ("Linux", Environments.Name(Environments.Linux))
    print printFormat % ("Windows", Environments.Name(Environments.Windows))
    print printFormat % ("OSX", Environments.Name(Environments.OSX))
    print printFormat % ("ATV2", Environments.Name(Environments.ATV2))
    print printFormat % ("ATV2", Environments.Name(Environments.TVOS))
    print printFormat % ("IOS", Environments.Name(Environments.IOS))
    print printFormat % ("Android", Environments.Name(Environments.Android))
    print printFormat % ("Apple", Environments.Name(Environments.Apple))
    print printFormat % ("Google", Environments.Name(Environments.Google))
    print printFormat % ("All", Environments.Name(Environments.All))
