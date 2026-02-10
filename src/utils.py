import json


def extract_substring_between(text : str, start_substring: str, end_substring: str):
    """ Extracts a substring between two given substring markers and given a given string """ 
    temporary_container = text.split(start_substring)
    temporary_container = temporary_container[1].split(end_substring)
    target_substring = temporary_container[0]
    return target_substring #Returns target substring   

def check_master_records(url = str):
    """This method takes a string (Tabelog URL JP) and checks if it exists in my master records
    Method will return none if the place is not on my records, otherwise it returns the json data for that restaurant"""

    with open('./data/url_map.json', 'r', encoding='utf-8') as json_data: #Opening our master file
        master_table = json.load(json_data) #Loading it as a dictionary in python 
        place_id = master_table.get(url)#Does it exist? if so place_id is the place_id 
    if place_id:#if it does, lets return the json file. 
        restaurant_json = load_restaurant_json(place_id)       
        return restaurant_json
    else: #if it doesn't exist, let's add it to our records
        return None
        
def combine_two_dictionaries(dict_name1: str, dict_name2: str, dict1: dict, dict2: dict):
    combined_dict = {dict_name1:dict1,
                     dict_name2:dict2
    }
    return combined_dict



def load_restaurant_json(google_id = str):
    file_path = f"./data/master_cache/{google_id}.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        restaurant_json = json.load(f)
    return restaurant_json



def add_to_records(combined_dict):

    tabelog_url = combined_dict["Tabelog"]["URL"] 
    google_id = combined_dict["Google"]["id"]

    file_path = f"./data/master_cache/{google_id}.json"

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(combined_dict, f, ensure_ascii=False, indent=4)
    #dumps new json file yay 




    #updating the master tracker, we do read and write separately as json sucks ass sometimes
    with open("./data/url_map.json", 'r', encoding='utf-8') as f:
        url_map = json.load(f)
    
    # Add the new link
    url_map[tabelog_url] = google_id
    
    # Save the updated map back to disk
    with open("./data/url_map.json", 'w', encoding='utf-8') as f:
        json.dump(url_map, f, ensure_ascii=False, indent=4)
        
    return True
    
