class raw_data:
    def __init__(self, rawDataName, rawDataData, rawDataDataContentType, rawDataSubType, rawDataCoordinates, rawDataContent,
                 rawDataSourceType, rawDataSourceUri, rawDataCreationDate):
        # INDISPENSABLE
        self.rawDataName = rawDataName

        # Pour les images
        self.rawDataData = rawDataData
        self.rawDataDataContentType = rawDataDataContentType
        self.rawDataSubType = rawDataSubType

        self.rawDataCoordinates = rawDataCoordinates

        self.rawDataContent = rawDataContent

        self.rawDataSourceType = rawDataSourceType

        self.rawDataSourceUri = rawDataSourceUri

        self.rawDataCreationDate = rawDataCreationDate
