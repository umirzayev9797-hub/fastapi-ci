from flask import Flask, url_for, render_template_string

app = Flask(__name__)

@app.route('/dogs')
def dogs():
    return 'Страница с пёсиками'

@app.route('/cats')
def cats():
    return 'Страница с котиками'

@app.route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'

@app.route('/index')
def index():
    return 'Главная страница'

# --- Error Handler для 404 ---
@app.errorhandler(404)
def page_not_found(e):
    # получаем все маршруты приложения
    links = []
    for rule in app.url_map.iter_rules():
        # исключаем служебные маршруты типа static
        if "GET" in rule.methods and len(rule.arguments) == 0:
            links.append(f'<li><a href="{rule.rule}">{rule.rule}</a></li>')

    html = f"""
    <h1>Страница не найдена (404)</h1>
    <p>Доступные страницы:</p>
    <ul>
        {''.join(links)}
    </ul>
    """
    return render_template_string(html), 404

if __name__ == '__main__':
    app.run(debug=True)
