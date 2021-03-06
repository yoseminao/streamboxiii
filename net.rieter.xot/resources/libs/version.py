#===============================================================================
# LICENSE Retrospect-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================


class Comparable:
    """ 
    Base Class for a simple comparison class. A derived class only needs to
    implement an __lt__(self, other) method. All the other required methods are
    implemented by this Comparable class and are based on the __lt__ method.
    
    """

    def __init__(self):
        pass

    def __eq__(self, other):
        """ Test two objects 'for Equality'
        
        Arguments:
        other : Object - The other object.
        
        Returns:
        True or False
        
        """

        if other is None:
            return False

        return not self < other and not other < self

    def __ne__(self, other):
        """ Test two objects 'for non-equality'  
        
        Arguments:
        other : Object - The other object.
        
        Returns:
        True or False
        
        """

        return not self.__eq__(other)

    def __gt__(self, other):
        """ Test two objects for 'greater than'
        
        Arguments:
        other : Object - The other object.
        
        Returns:
        True or False
        
        """

        if other is None:
            return True

        return other < self

    def __ge__(self, other):
        """ Test two objects for 'greater or equal than'  
        
        Arguments:
        other : Object - The other object.
        
        Returns:
        True or False
        
        """

        return not self < other

    def __le__(self, other):
        """ Test two objects for 'less than or equal'
        
        Arguments:
        other : Object - The other object.
        
        Returns:
        True or False
        
        """

        return not other < self


class Version(Comparable):
    """ Class representing a version number """

    def __init__(self, version=None, major=None, minor=None, build=None,
                 revision=None, build_type=None):
        """ Initialises a new version number

        :param str version:     Version string
        :param int major:       The Major build number
        :param int minor:       The Minor build number
        :param int build:       The Build number
        :param int revision:    The Revision number
        :param str build_type:  None, Alpha, Beta etc

        """

        Comparable.__init__(self)

        if version is None and major is None and minor is None and revision is None and build is None:
            raise ValueError("Either a version string or a set of version numbers should be provided.")

        if version and not (major is None and minor is None and revision is None and build is None):
            raise ValueError("Only a complete version or a set of version numbers should be provided, not both.")

        if major is None and not (minor is None and revision is None and build is None):
            raise ValueError("A Major version must be provided if a minor, revision or build is provided.")

        if minor is None and not (revision is None and build is None):
            raise ValueError("A Minor version must be provided if a revision or build is provided.")

        if build is None and revision is not None:
            raise ValueError("A build number must be provided if a revision is provided.")

        self.major = major
        self.minor = minor
        self.revision = revision
        self.build = build
        if build_type is not None:
            self.buildType = build_type.lower()
        else:
            self.buildType = None

        if version:
            self.__extract_version(version)

    def equal_builds(self, other):
        """ Checks if two versions have the same version up until the revision 
        part of the version.
        
        :param Version other:   The version to compare with.

        :return: True if equal.
        :rtype: bool

        """

        if other is None:
            return False

        return self.major == other.major and self.minor == other.minor and self.build == other.build

    def __extract_version(self, version):
        """ Extracts the Major, Minor, Revision and Buildnumber from a version string
        
        :param str|unicode version: The version string.

        :rtype: None

        """

        if "~" in version:
            version, self.buildType = version.split("~")

        split = str(version).split('.')
        if len(split) > 0:
            self.major = int(split[0])
        if len(split) > 1:
            self.minor = int(split[1])
        if len(split) > 2:
            self.build = int(split[2])
        if len(split) > 3:
            self.revision = int(split[3])

    def __none_is_zero(self, value):
        """ Returns 0 if a value is None. This is needed for comparison. As None
        should be interpreted as Zero. 
        
        :param int value: The value to check for None

        :return: 0 if the value was None
        :rtype: int

        """

        if value is None:
            return 0
        return int(value)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """ String representation """

        if self.major is None:
            return "None"

        if self.buildType:
            if self.minor is None:
                return "%d~%s" % (self.major, self.buildType)
            elif self.build is None:
                return "%d.%d~%s" % (self.major, self.minor, self.buildType)
            elif self.revision is None:
                return "%d.%d.%d~%s" % (self.major, self.minor, self.build, self.buildType)
            else:
                return "%d.%d.%d.%d~%s" % (self.major, self.minor, self.build, self.revision, self.buildType)
        else:
            if self.minor is None:
                return str(self.major)
            elif self.build is None:
                return "%d.%d" % (self.major, self.minor)
            elif self.revision is None:
                return "%d.%d.%d" % (self.major, self.minor, self.build)
            else:
                return "%d.%d.%d.%d" % (self.major, self.minor, self.build, self.revision)

    def __lt__(self, other):
        """ Tests two versios for 'Lower Then' 
        
        Arguments:
        other : Version - The version to compare with.
        
        Returns:
        True or False

        """

        version_types = ["alpha", "beta"]

        if other is None:
            return False

        if not self.__none_is_zero(self.major) == self.__none_is_zero(other.major):
            return self.__none_is_zero(self.major) < self.__none_is_zero(other.major)

        if not self.__none_is_zero(self.minor) == self.__none_is_zero(other.minor):
            return self.__none_is_zero(self.minor) < self.__none_is_zero(other.minor)

        if not self.__none_is_zero(self.build) == self.__none_is_zero(other.build):
            return self.__none_is_zero(self.build) < self.__none_is_zero(other.build)

        if not self.__none_is_zero(self.revision) == self.__none_is_zero(other.revision):
            return self.__none_is_zero(self.revision) < self.__none_is_zero(other.revision)

        if self.buildType is None and other.buildType is None:
            # they are the same
            return False

        if self.buildType is None and other.buildType is not None:
            # one has beta/alpha, the other None, so the other is larger
            return False

        if self.buildType is not None and other.buildType is None:
            return True

        # we have 2 build types
        self_build_name = self.buildType.rstrip("0123456789")
        self_build_name_number = self.buildType.lstrip("".join(version_types)) or "0"
        other_build_name = other.buildType.rstrip("0123456789")
        other_build_name_number = other.buildType.lstrip("".join(version_types)) or "0"

        if self_build_name == other_build_name:
            return int(self_build_name_number) < int(other_build_name_number)

        return version_types.index(self_build_name) < version_types.index(other_build_name)
