if __name__ == "__main__":
    from constants import domains, selected_domains
    from tools.segregate import splitIntoDomains, getDatasetOfDomain
    from tools.convert import convertDialogs, fixAddress
    from tools.write import writeSplitDatasetToJson
    from tools.translate import translateDialogs
    import constants

    path = "database/multiwoz_2.1.json"
    dataset = splitIntoDomains(path, domains, selected_domains)
    req_dataset = getDatasetOfDomain(selected_domains, dataset)
    fixAddress(
        req_dataset.T,
        ['attraction']
    )
    convertDialogs(
        req_dataset.T,
        [
            {
                "name": "database/Taxi_Database.xlsx",
                "ontology": constants.taxi_ontology,
            },
            {
                "name": "database/Restaurant_Database.xlsx",
                "ontology": constants.restaurant_ontology,
            },
            {
                "name": "database/Attraction_Database.xlsx",
                "ontology": constants.attraction_ontology,
            },
        ],
        ["Taxi-Inform", "Restaurant-Inform", "Attraction-Inform"],
        constants.selected_domains,
    )
    writeSplitDatasetToJson(dataset, True)
    translateDialogs(dataset)

