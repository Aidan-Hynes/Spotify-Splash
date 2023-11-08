from flask import Flask, request, redirect, render_template, session, jsonify
import secrets
import Spotify_Control as sc
import Process_Colour as pc

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)


@app.route("/")
def auth():
    url = sc.get_user_auth()
    return redirect(url)


@app.route("/callback")
def get_token():
    auth_code = request.args.get('code')
    access_token, refresh_token = sc.get_first_token(auth_code)

    code_file = open("code.txt", "w")
    code_file.writelines([access_token, '\n', refresh_token])
    code_file.close()

    return "<h1>You may now close the page<h1/>"


@app.route("/running", methods=['GET', 'POST'])
def run():
    code_file = open("code.txt", "r")
    access_token, refresh_token = code_file.readlines()
    code_file.close()

    access_token = access_token.strip()
    refresh_token = refresh_token.strip()

    print(access_token)
    print(refresh_token)

    try:
        cover_info = sc.get_album_cover(access_token)
    except:
        try:
            access_token = sc.get_new_token(refresh_token)
            cover_info = sc.get_album_cover(access_token)
        except:
            print('unknown code error')
            return "<h1>Error<h1/>", 404

    if cover_info is not None:
        rgb_value = pc.get_rgb_value(cover_info)
        return jsonify(rgb_value)

    return render_template('run.html')
