if __name__ == "__main__":
    from constants import domains,selected_domains
    from tools.segregate import splitIntoDomains,getDatasetOfDomain
    from tools.convert import convertDialogActs
    from tools.write import writeSplitDatasetToJson
    import constants
    path = input('Enter Dataset Path : ')
    dataset = splitIntoDomains(path,domains,selected_domains)
    req_dataset = getDatasetOfDomain(selected_domains,dataset)
    convertDialogActs(req_dataset.T,'database/Taxi_Database.xlsx',constants.taxi_ontology,['Taxi-Inform'])
    convertDialogActs(req_dataset.T,'database/Restaurant_Database.xlsx',constants.restaurant_ontology,['Restaurant-Inform'])
    convertDialogActs(req_dataset.T,'database/Attraction_Database.xlsx',constants.attraction_ontology,['Attraction-Inform'])
    writeSplitDatasetToJson(dataset,True)
