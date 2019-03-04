#===============================================================================
# LICENSE Retrospect-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================

from regexer import Regexer
from helpers.taghelperbase import TagHelperBase

#===============================================================================
# Make global object available
#===============================================================================
from logger import Logger


class XmlHelper(TagHelperBase):
    """Class that helps getting the content of XML nodes"""

    def get_single_node_content(self, node_tag, *args, **kwargs):
        """Retreives a single node 
        
        Arguments:
        nodeTag : string     - Name of the node to retrieve 
        args    : dictionary - Dictionary holding the node's attributes. Should
                               occur in order of appearance.
        
        Keyword Arguments:
        stripCData : Bool - If True the <![CDATA[......]]> will be removed.
        
        Returns:
        the content of the first match that is found.
        
        The args should be a dictionary: {"size": "380x285"}, {"ratio":"4:3"} 
        will find a node with <nodename size="380x285" name="test" ratio="4:3">
        
        """
        
        if "stripCData" in kwargs:
            strip_cdata = kwargs["stripCData"]
        else:
            strip_cdata = False
        
        result = self.get_nodes_content(node_tag, *args)
        if len(result) > 0:
            if strip_cdata:
                return XmlHelper.__strip_cdata(result[0])
            else:
                return result[0]
        else:
            return ""
    
    def get_nodes_content(self, node_tag, *args):
        """Retreives all nodes with nodeTag as name 
        
        Arguments:
        nodeTag : string     - Name of the node to retrieve 
        args    : dictionary - Dictionary holding the node's attributes. Should
                               occur in order of appearance.
        
        Returns:
        A list of all the content of the found nodes.
        
        The args should be a dictionary: {"size": "380x285"}, {"ratio":"4:3"} 
        will find a node with <nodename size="380x285" name="test" ratio="4:3">
        
        """
        
        regex = "<%s" % (node_tag,)
        
        for arg in args:
            regex += '[^>]*%s\W*=\W*"%s"' % (arg.keys()[0], arg[arg.keys()[0]])
            # just do one pass

        regex += "[^>]*>([\w\W]+?)</%s>" % (node_tag,)
        Logger.trace("XmlRegex = %s", regex)
        
        #regex = '<%s>([^<]+)</%s>' % (nodeTag, nodeTag)
        results = Regexer.do_regex(regex, self.data)
        Logger.trace(results)
        return results
    
    @staticmethod
    def __strip_cdata(data):
        """ Strips the <![CDATA[......]]> from XML data tags 
        
        Arguments:
        data : String - The data to strip from.
        
        """
        
        #Logger.Debug(data)
        #Logger.Debug(data.replace("<![CDATA[","").replace("]]>",""))
        return data.replace("<![CDATA[", "").replace("]]>", "")
