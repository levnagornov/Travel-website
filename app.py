from flask import Flask, render_template
import data

app = Flask(__name__)

@app.route('/')
def render_index():
    ''' Main page '''
    return render_template(
        'index.html', 
        title=data.title, 
        subtitle=data.subtitle, 
        description=data.description,
        all_departures=data.departures,
        all_tours=data.tours
    )


@app.route('/data/departures/<departure>/')  
def render_departures(departure):
    ''' Page shows all possible tours by certain departure '''

    if departure not in data.departures:
        return render_not_found(404)

    return render_template(
        'departure.html',
        title=data.title,  
        departure=departure, 
        all_tours=data.tours, 
        all_departures=data.departures
    )


@app.route('/data/tours/<tour_id>/')
def render_tours(tour_id):
    ''' Page of certain tour '''

    if data.tours.get(int(tour_id), 0) == 0:
        return f'К сожалению, тура с номером {tour_id} не существует, попробуйте снова.'

    return render_template(
        'tour.html', 
        title=data.title,
        tour_info=data.tours.get(int(tour_id)),
        all_departures=data.departures   
    )


@app.route('/data/')
def render_data():
    ''' TEMPORARY PAGE. Show all accessible tours '''

    return render_template('data.html', all_tours=data.tours)


#errors handling
@app.errorhandler(500)
def render_server_error(error):
    ''' Handling 500 error '''

    return "Что-то не так, но мы все починим"

@app.errorhandler(404)
def render_not_found(error):
    ''' Handling 404 error '''

    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!"   


if __name__ == '__main__':
    app.run(debug=True)