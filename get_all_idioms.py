from webapp import create_app
from webapp.native_english_idioms import get_links_to_themes, get_python_idioms, save_idioms

app = create_app()
with app.app_context():
        list_of_themes = get_links_to_themes()
        for theme in list_of_themes:
            get_python_idioms(theme['name_of_theme'], theme['link_to_theme'])
