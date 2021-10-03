import requests
import json


def getFlightData(dep_iata, dest_iata, date_dep, seat_class):
    departure = dep_iata.upper()
    destination = dest_iata.upper()
    requestData = requests.get(
        f"https://american-airlines-api.herokuapp.com/flights?date={date_dep}&origin={departure}&destination={destination}")
    parsedData = json.loads(requestData.content)
    final_list = []

    for i in range(len(parsedData)):
        distance = int(parsedData[i]['distance']) * 1.60934
        flight_num = parsedData[i]['flightNumber']
        passenger = parsedData[i]['aircraft']['passengerCapacity']['total']
        depart = parsedData[i]['departureTime']

        if int(depart[11:13]) < 12:
            depart_time = depart[11:16] + " AM"
        elif int(depart[11:13]) < 22:
            depart_time = "0" + str(int((depart[11:13])) - 12) + str(depart[13:16]) + " PM"
        else:
            depart_time = str(int((depart[11:13])) - 12) + str(depart[13:16]) + " PM"

        depart_date = depart[0:10]

        arrive = parsedData[i]['arrivalTime']
        arrive_time = arrive[11:16]
        arrive_date = arrive[0:10]
        if int(arrive[11:13]) < 12:
            arrive_time = arrive[11:16] + " AM"
        elif int(arrive[11:13]) < 22:
            arrive_time = "0" + str(int((arrive[11:13])) - 12) + str(arrive[13:16]) + " PM"
        else:
            arrive_time = str(int((arrive[11:13])) - 12) + str(arrive[13:16]) + " PM"

        if distance < 2000:
            if seat_class == 1:
                price = "$300-$400"
            elif seat_class == 2:
                price = "$450-$675"
            elif seat_class == 3:
                price = "$900-$1200"
        elif 2000 < distance < 4000:
            if seat_class == 1:
                price = "$400-$500"
            elif seat_class == 2:
                price = "$600-$750"
            elif seat_class == 3:
                price = "$1200-$1500"
        elif 4000 < distance < 6000:
            if seat_class == 1:
                price = "$500-$600"
            elif seat_class == 2:
                price = "$750-$900"
            elif seat_class == 3:
                price = "$1500-$1800"
        elif 6000 < distance < 8000:
            if seat_class == 1:
                price = "$600-$700"
            elif seat_class == 2:
                price = "$900-$1050"
            elif seat_class == 3:
                price = "$1800-$2100"
        elif 8000 < distance < 10000:
            if seat_class == 1:
                price = "$700-$800"
            elif seat_class == 2:
                price = "$1050-$1200"
            elif seat_class == 3:
                price = "$2100-$2400"
        else:
            if seat_class == 1:
                price = "900+"
            elif seat_class == 2:
                price = "$1350+"
            elif seat_class == 3:
                price = "$2700+"

        temp_list = [flight_num, round(distance, 2), passenger, depart_date, depart_time, arrive_date, arrive_time,
                     price]
        final_list.append(temp_list)
    return final_list


def getEmissions(distanceGreaterCircleKM, seatClass):
    # DISTANCE HAS THE 95 KM DC CONSTANT ADDED TO IT
    distanceGreaterCircleKM = int(distanceGreaterCircleKM) + 95

    # CHECK IF THE FLIGHT IS A SHORT HAUL
    if distanceGreaterCircleKM < 1500:
        # CHECK TO SEE WHAT THE SEAT FACTOR OF THE FLIGHT IS
        if seatClass == 1:
            seatFactor = 0.96
        elif seatClass == 2:
            seatFactor = 1.26
        elif seatClass == 3:
            seatFactor = 2.40
        emissionsPerPerson = ((((2.714 * distanceGreaterCircleKM) + 1166.52) / 125.8782) * 0.93 * seatFactor * 6.84) + (
                0.00038 * distanceGreaterCircleKM) + 11.68
        return emissionsPerPerson

    # CHECK IF THE FLIGHT IS A LONG HAUL
    elif distanceGreaterCircleKM > 2500:
        # CHECK TO SEE WHAT THE SEAT FACTOR OF THE FLIGHT IS
        if seatClass == 1:
            seatFactor = 0.80
        elif seatClass == 2:
            seatFactor = 1.54
        elif seatClass == 3:
            seatFactor = 2.40
        emissionsPerPerson = ((((.0001 * pow(distanceGreaterCircleKM, 2)) + (
                7.104 * distanceGreaterCircleKM) + 5044.93) / (280.21 * .82)) * .74 * seatFactor * (
                                      (3.15 * 2) + .54)) + (
                                     0.00038 * distanceGreaterCircleKM) + 11.68
        return emissionsPerPerson

    # CALCULATING THE INTERPOLATED EMISSIONS FOR A FLIGHT BETWEEN 1500 AND 2500 KM
    elif 1500 < distanceGreaterCircleKM < 2500:

        # FIND THE SEAT FACTOR FOR THE SHORT HAUL
        if seatClass == 1:
            seatFactor = 0.96
        elif seatClass == 2:
            seatFactor = 1.26
        elif seatClass == 3:
            seatFactor = 2.40

        # FIND THE EMISSIONS OF THE FLIGHT WITH A SHORT-HAUL
        shortHaulEmissions = ((5234.806 / 125.8782) * seatFactor * 6.3612) + 12.24962  # SHORT HAUL USES 1499 KM

        # FIND THE SEAT FACTOR FOR THE LONG HAUL
        if seatClass == 1:
            seatFactor = 0.80
        elif seatClass == 2:
            seatFactor = 1.54
        elif seatClass == 3:
            seatFactor = 2.40

        # FIND THE EMISSIONS OF THE FLIGHT WITH A LONG-HAUL
        longHaulEmissions = ((22812.2841 / 29.72) * seatFactor * 5.0616) + 12.63038  # LONG HAUL USES 2501 KM

        # INTERPOLATE USING THE DISTANCE AND THE TWO POINTS WITH THE SEAT CLASS
        interpolatedEmissions = shortHaulEmissions + (
                (distanceGreaterCircleKM - 1499) * ((longHaulEmissions - shortHaulEmissions) / 1000))
        return interpolatedEmissions
