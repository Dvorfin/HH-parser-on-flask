from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from hh_api import HHApi
from functions import write_requests_into_txt, get_last_request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parser_database.db'
db = SQLAlchemy(app)
hh_connection = HHApi()  # создаем подключение к api hh.ru
# just comment to delete


class Vacancies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    salary = db.Column(db.String(50), nullable=True)
    vac_type = db.Column(db.String(50), nullable=True)
    published_at = db.Column(db.DateTime, nullable=True)
    employer = db.Column(db.String(100), nullable=True)
    requirement = db.Column(db.Text, nullable=True)
    responsibility = db.Column(db.Text, nullable=True)
    vacancy_url = db.Column(db.String(100), nullable=True)
    experience = db.Column(db.String(50), nullable=True)
    employment = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return '<Vacancies %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
@app.route('/page', methods=['GET', 'POST'])
@app.route('/page/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    # vacancies = Vacancies.query.order_by(Vacancies.published_at.desc()).limit(10).offset(page * 10)
    vacancies = Vacancies.query.order_by(Vacancies.published_at.desc()).paginate(page=page, per_page=10)
    print(vacancies.prev())
    print(vacancies.page)
    print(list(vacancies.iter_pages()))
    return render_template('index.html', vacancies=vacancies)


@app.route('/refresh', methods=['POST', 'GET'])
def refresh():
    last_request = get_last_request()
    default_request_text = hh_connection.get_text()

    if request.method == 'POST':
        request_text = request.form.get('request_text')

        if len(request_text) == 0:  # если не задан реквест, то используется текст из поля
            request_text = default_request_text

        hh_connection.set_text(request_text)
        hh_connection.make_request()  # отправялем реквест
        data = hh_connection.get_data()  # получаем данные

        vacancies_value = hh_connection.get_value_found_vacancies()
        is_req = False

        # проходимся по всем страницам реквеста к хх
        for page in range(0, hh_connection.get_total_pages() + 1):

            for item in data['items']:
                data_to_load = HHApi.filter_data_from_hh(item)

                # проверяем наличие данной вакансии в БД

                exists = Vacancies.query.filter_by(vacancy_url=data_to_load[-3]).first() is not None
                if exists:
                    continue

                tmp = ['name', 'salary', 'vac_type', 'published_at', 'employer',
                       'requirement', 'responsibility', 'vacancy_url', 'experience', 'employment']
                data_to_load = {k: v for k, v in zip(tmp, data_to_load)}

                vacancies = Vacancies(**data_to_load)

                try:  # пробуем добавить инфу в бд
                    db.session.add(vacancies)
                    db.session.commit()
                except Exception as e:
                    return f"При добавлении статьи произошла ошибка: {e}"

            save_request = request.form.get('save_request')
            if save_request == '1':
                write_requests_into_txt(request_text)

            last_request = request_text     # текст последнего запроса
            is_req = True

            hh_connection.set_page(page)    # увеличваем номер страницы
            hh_connection.make_request()  # отправялем реквест
            data = hh_connection.get_data()  # получаем данные

        return render_template('refresh.html', last_request=last_request, is_req=is_req,
                               vacancies_value=vacancies_value, default_request_text=default_request_text)

    return render_template('refresh.html', last_request=last_request, default_request_text=default_request_text)


if __name__ == '__main__':
    app.run(debug=True)
