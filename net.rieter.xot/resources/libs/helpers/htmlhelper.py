#===============================================================================
# LICENSE Retrospect-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================

import re

from regexer import Regexer
from helpers import taghelperbase


class HtmlHelper(taghelperbase.TagHelperBase):
    """Class that could help with parsing of simple HTML"""

    __ToTextRegex = None
    
    def get_tag_content(self, tag, *args, **kwargs):
        """Gets the content of an HTML <tag> 

        @param tag:     string     - name of tag to search for.
        @param args:    dictionary - each argument is interpreted as a html
                                     attribute. 'cls' is translated to class
                                     attribute. The attribute with value None
                                     is retrieved.
        @param kwargs:
          first_only:   boolean    - [opt] only return the first result. Default: True

        @return: The content of the found tag. If no match is found an empty string is
        returned.

        Example: ('div', {'cls':'test'}, {'id':'divTest'}) will match
        <div class="test" id="divTest">...content...</div>

        """
        
        first_only = True
        if kwargs.keys().count("first_only") > 0:
            first_only = kwargs["first_only"]

        html_regex = "<%s" % (tag,)
                
        for arg in args:
            name = arg.keys()[0]
            value = arg[arg.keys()[0]]

            # to keep working with older versions where class could not be passed
            if name == "cls":
                name = "class"

            html_regex += '[^>]*%s\W*=\W*["\']%s["\']' % (name, value)

        html_regex += "[^>]*>([^<]+)</"
        result = Regexer.do_regex(html_regex, self.data)
        if len(result) > 0:
            if first_only:
                return result[0].strip()
            else:
                return result
        else:
            return ""

    @staticmethod
    def to_text(html):
        # type: (str) -> object
        """ Converts HTML to text by replacing the HTML tags.

        @param html: string - HTML text input
        @return:     string - Plain text representation of the HTML

        """

        if html is None:
            return html

        if not HtmlHelper.__ToTextRegex:
            HtmlHelper.__ToTextRegex = re.compile('</?([^ >]+)(?: [^>]+)?>',
                                                  re.DOTALL + re.IGNORECASE)

        text = HtmlHelper.__ToTextRegex.sub(HtmlHelper.__html_replace, html)
        return text.replace("  ", " ")

    @staticmethod
    def __html_replace(match):
        tag = match.group(1).lower()
        if tag == 'br':
            return '\n'
        return ''
