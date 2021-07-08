from flask import Flask, render_template
import data, random, requests


app = Flask(__name__)


def get_weather_forcast(place):
    """Will return weather API of OpenWeatherMap"""
    api_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': place,
        'appid': '41c94dc66a745d6f4f245f158b18e871',
        'units': 'metric',
        "lang" : "ru",
    }
    res = requests.get(api_url, params=params)
    print(res.ok)
    if res.ok:
        res = res.json()
        weather = {
            "place" : place,
            "temperature" : res["main"]["temp"],
            "description" : res["weather"][0]["description"],
            "icon" : res["weather"][0]["icon"],
        }        
        return weather


@app.route("/")
def render_index():
    """Main page"""

    # 6 random tours for main page
    random_tours_id = random.sample(list(data.tours), k=6)
    random_tours = {
        num_of_tour: tour_info
        for num_of_tour, tour_info in data.tours.items()
        if num_of_tour in random_tours_id
    }

    return render_template(
        "index.html",
        title=data.title,
        subtitle=data.subtitle,
        description=data.description,
        all_departures=data.departures,
        all_tours=random_tours,
    )


@app.route("/data/departures/<departure>/")
def render_departures(departure):
    """Page shows all possible tours by certain departure"""

    if departure not in data.departures:
        message = (
            f"К сожалению, отправления из {departure} не существует, попробуйте снова."
        )
        return render_not_found(404, message)

    tours_by_departure = {
        num_of_tour: tour_info
        for num_of_tour, tour_info in data.tours.items()
        if tour_info["departure"] in departure
    }
    analitcs_of_found_tours = {
        "tours_found": len(tours_by_departure),
        "prices": [v["price"] for k, v in tours_by_departure.items()],
        "nights": [v["nights"] for k, v in tours_by_departure.items()],
    }

    return render_template(
        "departure.html",
        title=data.title,
        departure=departure,
        all_tours=tours_by_departure,
        all_departures=data.departures,
        analitics=analitcs_of_found_tours,
    )


@app.route("/data/tours/<int:tour_id>/")
def render_tours(tour_id):
    """Page of certain tour"""

    tour_info = data.tours.get(tour_id)
    if tour_info is None:
        message = (
            f"К сожалению, тура с номером {tour_id} не существует, попробуйте найти другой тур."
        )
        return render_not_found(404, message)

    place = tour_info["country"][1]
    return render_template(
        "tour.html",
        title=data.title,
        tour_info=tour_info,
        all_departures=data.departures,
        weather=get_weather_forcast(place),
    )


@app.route("/data/")
def render_data():
    """TEMPORARY PAGE due to the requirement of the course. Show all accessible tours"""

    return render_template("data.html", all_tours=data.tours)


# errors handling
@app.errorhandler(500)
def render_server_error(error, message="Что-то не так, но мы все починим!"):
    """Handling 500 error"""

    return render_template(
        "error.html", message=message, title=data.title, all_departures=data.departures
    )


@app.errorhandler(404)
def render_not_found(
    error, message="Ничего не нашлось! Вот неудача, отправляйтесь на главную!"
):
    """Handling 404 error"""

    return render_template(
        "error.html", message=message, title=data.title, all_departures=data.departures
    )


# entry point
if __name__ == "__main__":
    app.run(debug=True)
