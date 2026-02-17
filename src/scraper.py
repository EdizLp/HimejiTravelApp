from bs4 import BeautifulSoup
from .utils import extract_substring_between #use . as we run this from main, the . tells python look in the same folder as this module 
from .gemini_api import prompt_gemini



def core_tabelog_information(soup: BeautifulSoup):
    """This takes a BeautifulSoup object as it's argument (Tabelog website) and returns a dictionary with the Name, Address, Coords, Rating and URL from the Tabelog Page"""
    """Name: String, Address: String, Coords: Tuple, Rating: Float, URL: String"""
    restaurant_name_header = soup.find("h2", class_= "display-name") #Grabbing where the information is stored, if they change the html this needs to all change
    restaurant_rating_score = soup.find("span", class_= "rdheader-rating__score-val-dtl") 
    restaurant_address_container = soup.find("p", class_= "rstinfo-table__address") 
    restaurant_coord_container = soup.find("img", class_="rstinfo-table__map-image")
    canonical_tag = soup.find("link", rel="alternate", hreflang = "ja")             #Find the link for the Japanese site (This will work for any language.)
    reservation_status_td = soup.find("th", string="予約可否").find_next("td")   
    opening_hours_td = soup.find("th", string="営業時間").find_next("td")               #Find the table with that header, then find the next td tag




    try:
        reservation_info = reservation_status_td.get_text("\n", strip=True)      
    except AttributeError:
        reservation_info = "N/A"


    

    try:
        opening_hours = opening_hours_td.get_text("\n", strip=True)
    except AttributeError:
        opening_hours = "N/A"


    try:
        tabelog_url = canonical_tag["href"] #Using find as the link is inside the tags as opposed to .get_text()
    except AttributeError:
        tabelog_url = "N/A"

    try: #if soup cannot find the rating then it will return none
        rating_of_restaurant = restaurant_rating_score.get_text().strip()#Get returns everything outside of the tags etc
    except AttributeError:
        rating_of_restaurant = "N/A"

    try: #if soup cannot find the name then it will return none
        restaurant_name = restaurant_name_header.get_text().strip()
    except AttributeError:
        restaurant_name = "N/A"

    try: #Checks if it can find the address
        address_of_restaurant = restaurant_address_container.get_text().strip()#Get returns everything outside of the tags etc
    except AttributeError:
        address_of_restaurant ="N/A"


    try:
        restaurant_coords = restaurant_coord_container.get("data-lazy-src")#This gets the container tabelog uses for the url 
        restaurant_coords = extract_substring_between(restaurant_coords, "center=", "&style")
        restaurant_coords = restaurant_coords.split(",") #Doing this to separate longitude and latitude to turn it into a tuple.
        latitude = float(restaurant_coords[0])
        longitude = float(restaurant_coords[1])
        restaurant_coords_tup = (latitude, longitude)
        
    except AttributeError:
        restaurant_coords_tup = "N/A"

        


    info_to_translate = {
                      "Reservation":reservation_info,
                      "Opening_Hours":opening_hours
                      }
    translated_info = translate_information(info_to_translate)
    
    core_information = { #Dictionary containing the Coords, Address, Rating and Restaurant name 
        "Name":restaurant_name,
        "Rating":float(rating_of_restaurant),
        "Address":address_of_restaurant,
        "Coords":restaurant_coords_tup,
        "URL":tabelog_url,
        "Reservation":translated_info["Reservations"],
        "Resevation_Info":translated_info["Reservation_Info"],
        "Opening_Hours":translated_info["Opening_Hours"]
    } 
    return core_information 

def translate_information(info: dict):

    # We ask for JSON so your Python script can easily read it later
    prompt = f"""
    TASK: Extract and translate restaurant data to english.
    SOURCE TEXT:\n

    Reservation Information: {info["Reservation"]}\n
    Opening Hours: {info["Opening_Hours"]}

    INSTRUCTIONS:
    - Use "N/A" for missing fields.
    - Use 24-hour time format exclusively.
    """
    translation = prompt_gemini(prompt, "tabelog")
    print(translation)
    return translation


    
    
    






