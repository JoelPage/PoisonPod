import pp.external.xml.Utils as xmlUtils

class Settings():
    def __init__(self):
        self.m_dHostChannelID = ""
        self.m_dChannelID = ""
        self.m_xmlFilePath = "data/settings.xml"
        self.m_onlineEmoji = "✅"
        self.m_offlineEmoji = "❌"
        self.Load()

    def Load(self):
        try:
            xmlTree = xmlUtils.fileRead(self.m_xmlFilePath)
            root = xmlTree.getroot()
            settingsNode = xmlUtils.get_node(root, 'settings')
            
            self.m_dChannelID = xmlUtils.get_value_text(settingsNode, 'dChannelID')
            self.m_dHostChannelID = xmlUtils.get_value_text(settingsNode, 'dHostChannelID')
            self.m_onlineEmoji = xmlUtils.get_value_unicode(settingsNode, 'onlineEmoji')
            self.m_offlineEmoji = xmlUtils.get_value_unicode(settingsNode, 'offlineEmoji')
        except:
            pass

    def Save(self):
        root = xmlUtils.create_tree_root('root')
        settingsNode = xmlUtils.create_node(root, 'settings')

        xmlUtils.create_and_set_node_text_int_if_exists(settingsNode, 'dChannelID', self.m_dChannelID)
        xmlUtils.create_and_set_node_text_int_if_exists(settingsNode, 'dHostChannelID', self.m_dHostChannelID)
        xmlUtils.create_and_set_node_text_int_bytes(settingsNode, 'onlineEmoji', self.m_onlineEmoji)
        xmlUtils.create_and_set_node_text_int_bytes(settingsNode, 'offlineEmoji', self.m_offlineEmoji)

        xmlUtils.fileWrite(root, self.m_xmlFilePath)

    def GetChannelID(self):
        return self.m_dChannelID

    def GetHostChannelID(self):
        return self.m_dHostChannelID