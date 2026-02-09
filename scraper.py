from bs4 import BeautifulSoup
import googlemaps #For google Cloud interaction
#It's in the body, div id = "container"


def extract_substring_between(text : str, start_substring: str, end_substring: str):
    """ Extracts a substring between two given substring markers and given a given string """ 
    temporary_container = restaurantUrl.split(start_substring)
    temporary_container = temporary_container[1].split(end_substring)
    target_substring = temporary_container[0]
    return target_substring


def core_tabelog_information(soup: BeautifulSoup):
    """This takes a BeautifulSoup object as it's argument (Tabelog website) and returns a dictionary with the Name, Address, Coords and Rating from the Tabelog Page"""
    
    restaurantNameHeader = soup.find("h2", class_= "display-name") #Grabbing where the information is stored
    restaurantRatingScore = soup.find("span", class_= "rdheader-rating__score-val-dtl") 
    restaurantAddressContainer = soup.find("p", class_= "rstinfo-table__address") 
    restaurantCoordContainer = soup.find("img", class_="rstinfo-table__map-image")

    if restaurantNameHeader: #if soup cannot find the name then it will return none
        ratingOfRestaurant = restaurantRatingScore.get_text().strip()#Get returns everything outside of the tags etc
    else:
        ratingOfRestaurant = None

    if restaurantNameHeader: #if soup cannot find the name then it will return none
        nameOfRestaurant = restaurantNameHeader.get_text().strip()
    else:
        nameOfRestaurant = None

    if restaurantAddressContainer: #Checks if it can find the address
        address_of_restaurant = restaurantAddressContainer.get_text().strip()#Get returns everything outside of the tags etc
    else:
        address_of_restaurant = None

    if restaurantCoordContainer:
        restaurantUrl = restaurantCoordContainer.get("data-lazy-src")#This gets the url tabelog uses for the url 
        restaurantUrl = extract_substring_between(restaurantUrl, "center=", "&style")
    else:
        restaurantUrl = None

    core_information = {#Dictionary containing the Coords, Address, Rating and Restaurant name 
        "Name":nameOfRestaurant,
        "Rating":ratingOfRestaurant,
        "Address":address_of_restaurant,
        "Coords":None
    } 
    return core_information







with open('./test1.html', 'r', encoding='utf-8') as f: #Opening our test file using encoding for japanese characters
    tabelogData = f.read()
    soup = BeautifulSoup(tabelogData, 'html.parser') #Soup object for scraping with beautifulsoup



new = restaurantUrl.split("center=")
new2 = new[1].split("&style")
new3 = new2[0]
print(new3)


if restaurantNameHeader: #if soup cannot find the name then it will return none
    ratingOfRestaurant = restaurantRatingScore.get_text().strip()#Get returns everything outside of the tags etc
    print(ratingOfRestaurant)
else:
    print("F")

if restaurantNameHeader: #if soup cannot find the name then it will return none
    nameOfRestaurant = restaurantNameHeader.get_text().strip()
    print(nameOfRestaurant)
else:
    print("F")

if restaurantAddressContainer: #if soup cannot find the name then it will return none
    restaurantAddress = restaurantAddressContainer.get_text().strip()#Get returns everything outside of the tags etc
    print(ratingOfRestaurant)
else:
    print("F")