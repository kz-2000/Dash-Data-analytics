import dash
import dash_bootstrap_components as dbc
from layout.layout import create_layout
from callbacks.callbacks import register_callbacks
from dash_bootstrap_templates import load_figure_template


# Makes the Bootstrap Themed Plotly templates available
load_figure_template('vapor_dark')

# Initialize server
server = app.server

# Initialize the Dash app with the Quartz Bootstrap theme and Google Fonts
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.VAPOR,
    'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400&display=swap',
    '/assets/styles.css'
], suppress_callback_exceptions=True, server=server)


# Set the app layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)

