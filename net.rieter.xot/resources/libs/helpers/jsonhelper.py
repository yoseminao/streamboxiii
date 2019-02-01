# coding:UTF-8
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
import json


#noinspection PyShadowingNames
class JsonHelper:
    def __init__(self, data, logger=None):
        """Creates a class that wraps json.

        Arguments:
        data : string - JSON data to parse

        Keyword Arguments:
        Logger : Logger - If specified it is used for logging

        """
        self.logger = logger
        self.data = data.strip()
        self.json = dict()

        if len(self.data) == 0:
            # no data in, no data out
            self.json = dict()
            return

        if self.data[0] not in "[{":
            # find the actual start in case of a jQuery18303627530449324564_1370950605750({"success":true});
            if self.logger is not None:
                self.logger.debug("Removing non-Json wrapper")
            start = self.data.find("(") + 1
            end = self.data.rfind(")")
            self.data = self.data[start:end]

        # here we are call the json.loads
        self.json = json.loads(self.data)

    @staticmethod
    def convert_special_chars(text, do_quotes=True):
        """ Converts special characters in json to their Unicode equivalents. Quotes can
        be ommitted by specifying the doQuotes as False. The input text should be able to
        hold the output format. That means that for UTF-8 charachters
        to be allowed, the string should be UTF-8 decoded because, Python will otherwise
        assume it to be ASCII.

        Arguments:
        test     : string  - the text to search for.

        Keyword Arguments:
        doQuotes : Boolean - Should quotes be replaced

        Returns text with all the \uXXXX values replaced with their Unicode
        characters. XXXX is considered a Hexvalue. It returns unichr(int(hex)). The
        returnvalue is UTF-8 byte encoded.

        """

        # special chars
        # unicode chars
        clean_text = re.sub("(\\\u)(.{4})", JsonHelper.__special_chars_handler, text)

        # other replacements
        replacements = [("\\n", "\n"), ("\\r", "\r"), ("\\/", "/")]
        for k, v in replacements:
            clean_text = clean_text.replace(k, v)

        if do_quotes:
            clean_text = JsonHelper.__convert_quotes(clean_text)

        return clean_text

    @staticmethod
    def __convert_quotes(text):
        """ Replaces escaped quotes with their none escaped ones.

        Arguments:
        text : String - The input text to clean.

        """

        clean_text = text
        replacements = [('\\"', '"'), ("\\'", "'")]

        for k, v in replacements:
            clean_text = clean_text.replace(k, v)

        return clean_text

    @staticmethod
    def __special_chars_handler(match):
        """ Helper method to replace \uXXXX with unichr(int(hex))

        Arguments:
        match : RegexMatch - the matched element in which group(2) holds the
                             hex value.

        Returns the Unicode character corresponding to the Hex value.

        """

        hex_string = "0x%s" % (match.group(2))
        # print hexString
        hex_value = int(hex_string, 16)
        return unichr(hex_value)

    #noinspection PyUnboundLocalVariable
    def get_value(self, *args, **kwargs):
        """ Retrieves data from the JSON object based on the input parameters

        @param args:    the dictionary keys, or list indexes
        @param kwargs:  possible value = fallback and allows the specification of a fallback value

        @return: the selected JSON object

        """

        try:
            data = self.json
            for arg in args:
                data = data[arg]
        except KeyError:
            if "fallback" in kwargs:
                if self.logger:
                    self.logger.debug("Key ['%s'] not found in Json", arg)
                return kwargs["fallback"]

            if self.logger:
                self.logger.warning("Key ['%s'] not found in Json", arg, exc_info=True)
            return None

        return data

    @staticmethod
    def dump(dictionary, pretty_print=True):
        """ Dumps a JSON object to a string

        @param pretty_print:     (boolean) indicating if the format should be nice
        @param dictionary: (string) the object to dump

        @return: a valid JSON string
        """

        if pretty_print:
            return json.dumps(dictionary, indent=4)
        else:
            return json.dumps(dictionary)

    @staticmethod
    def loads(json_data):
        """ Loads a JSON object to a valid object

        @param json_data:   (string) the JSON data to load

        @return: a valid JSON object
        """

        return json.loads(json_data)

    def __str__(self):
        return self.data
