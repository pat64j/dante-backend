from flask import render_template
from core import create_app
from core.commands import create_tables, drop_tables, prune_tokens

app = create_app()

app.cli.add_command(create_tables)
app.cli.add_command(drop_tables)
app.cli.add_command(prune_tokens)

def start_ngrok():
    from pyngrok import ngrok
    url = ngrok.connect(5000)
    print('Tunnel URL: ', url)

if app.config['START_NGROK']:
    start_ngrok()


@app.route('/')
def myhome():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

