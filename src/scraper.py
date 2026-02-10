from bs4 import BeautifulSoup
from .utils import extract_substring_between #use . as we run this from main, the . tells python look in the same folder as this module 




def core_tabelog_information(soup: BeautifulSoup):
    """This takes a BeautifulSoup object as it's argument (Tabelog website) and returns a dictionary with the Name, Address, Coords, Rating and URL from the Tabelog Page"""
    """Name: String, Address: String, Coords: Tuple, Rating: Float, URL: String"""
    restaurantNameHeader = soup.find("h2", class_= "display-name") #Grabbing where the information is stored, if they change the html this needs to all change
    restaurantRatingScore = soup.find("span", class_= "rdheader-rating__score-val-dtl") 
    restaurantAddressContainer = soup.find("p", class_= "rstinfo-table__address") 
    restaurantCoordContainer = soup.find("img", class_="rstinfo-table__map-image")
    canonical_tag = soup.find("link", rel="canonical")#Can it find the canonical tag (it returns none if it can)


    if canonical_tag:
        tabelog_url = canonical_tag["href"] #Using find as the link is inside the tags as opposed to .get_text()
    else:
        tabelog_url = None

    if restaurantRatingScore: #if soup cannot find the rating then it will return none
        ratingOfRestaurant = restaurantRatingScore.get_text().strip()#Get returns everything outside of the tags etc

    if restaurantNameHeader: #if soup cannot find the name then it will return none
        nameOfRestaurant = restaurantNameHeader.get_text().strip()

    if restaurantAddressContainer: #Checks if it can find the address
        address_of_restaurant = restaurantAddressContainer.get_text().strip()#Get returns everything outside of the tags etc


    if restaurantCoordContainer: #Fix this formatting, it needs to be exactly how i want 
        restaurantCoords = restaurantCoordContainer.get("data-lazy-src")#This gets the container tabelog uses for the url 
        restaurantCoords = extract_substring_between(restaurantCoords, "center=", "&style")
        restaurantCoords = restaurantCoords.split(",") #Doing this to separate longitude and latitude to turn it into a tuple.
        latitude = float(restaurantCoords[0])
        longitude = float(restaurantCoords[1])
        restaurantCoordsTup = (latitude, longitude)
        
    else:
        restaurantCoordsTup = None

        



    core_information = {#Dictionary containing the Coords, Address, Rating and Restaurant name 
        "Name":nameOfRestaurant,
        "Rating":float(ratingOfRestaurant),
        "Address":address_of_restaurant,
        "Coords":restaurantCoordsTup,
        "URL":tabelog_url
    } 
    return core_information 

    
    
    






