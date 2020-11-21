import pp.external.xml.Utils as xmlUtils

class Settings():
    def __init__(self):
        self.m_dChannelID = ""
        self.m_xmlFilePath = "data/settings.xml"

    def Load(self, node):
        xmlTree = xmlUtils.fileRead(self.m_xmlFilePath)
        self.m_dChannelID = xmlUtils.get_value_text(node, 'dChannelID')

    def Save(self):
        root = xmlUtils.create_tree_root('root')
        settingsNode = xmlUtils.create_node(root, 'settings')
        print(settingsNode)
        
        xmlUtils.create_and_set_node_text_int_if_exists(settingsNode, 'dChannelID', self.m_dChannelID)

        xmlUtils.fileWrite(root, self.m_xmlFilePath)

    def GetChannelID(self):
        return self.m_dChannelID