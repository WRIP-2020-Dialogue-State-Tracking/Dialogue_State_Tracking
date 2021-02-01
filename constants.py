domains = ["attraction", "hospital", "hotel", "police", "restaurant", "taxi", "train"]
selected_domains = ["attraction", "restaurant", "taxi"]
taxi_ontology = ["departure", "destination"]
restaurant_ontology = [
    "name",
    "area",
    "pricerange",
    "food",
    "address",
    "phone",
    "postcode",
]
attraction_ontology = [
    "name",
    "area",
    "pricerange",
    "entrance_fee",
    "address",
    "openhours",
    "phone",
    "postcode",
    "type",
]
day_dictionary = {
    "monday": "सोमवार",
    "tuesday": "मंगलवार",
    "wednesday": "बुधवार",
    "thursday": "गुरूवार",
    "friday": "शुक्रवार",
    "saturday": "शनिवार",
    "sunday": "रविवार",
}
car_color_dictionary = {
    "black": "मिनी",
    "white": "मिनी",
    "red": "माइक्रो",
    "yellow": "माइक्रो",
    "blue": "सेडान",
    "grey": "सेडान",
}
car_type_dictionary = {
    "toyota": "हुंडई",
    "skoda": "मारुति सुजुकी",
    "bmw": "होंडा",
    "honda": "महिंद्रा",
    "ford": "रेनॉल्ट",
    "audi": "फोर्ड",
    "lexus": "जीप",
    "volvo": "टाटा",
    "volkswagen": "टोयोटा",
    "tesla": "स्कोडा",
}
import itertools

car_dictionary = {
    " ".join([_color, _type]): " ".join(
        [car_color_dictionary[_color], car_type_dictionary[_type]]
    )
    for _color, _type in itertools.product(
        car_color_dictionary.keys(), car_type_dictionary.keys()
    )
}