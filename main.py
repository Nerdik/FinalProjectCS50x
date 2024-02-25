'''Import additional functions from helpers.py'''
from helpers import get_city, get_date, get_coordinates, output_form


def main():
    '''Main function initiolization'''
    city = input("Input the City name: ")
    valid_city = get_city(city)

    date = input("Input the Day/Period (Today or Tomorrow or Week): ")
    valid_date = get_date(date)

    valid_lat = get_coordinates(valid_city)[0]
    valid_long = get_coordinates(valid_city)[1]

    output_form(valid_date, valid_city, valid_lat, valid_long)



if __name__ == "__main__":
    main()
