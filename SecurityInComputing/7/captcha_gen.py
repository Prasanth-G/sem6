from flask import *
from captcha.image import ImageCaptcha
import string
import random
import http.server
import os

def get_captcha(n=6):
    cap = ImageCaptcha()
    ch = "".join(random.choices(string.ascii_lowercase , k=n))
    img = cap.generate_image(ch)
    filename = "".join(random.choices(string.ascii_lowercase, k=6)) + ".png"
    img.save(filename)
    return filename, ch

stored_capt = ""
filename = ""
app = Flask(__name__, template_folder='.')

@app.route('/', methods=['GET'])
def handler():
    global filename, stored_capt
    if os.path.exists(filename):
        os.remove(filename)
    filename, stored_capt = get_captcha()
    print("*"*10, stored_capt)
    return render_template('index.html', captcha_filename=filename)
        
@app.route('/validate', methods=['POST'])
def validate():
    if request.form['char_captcha'] == stored_capt:
        return '<h1>Captcha Accepted</h1>'
    else:
        return '<h1>GO back & Try again</h1>'

@app.route("/<filename>")
def get_captcha_img(filename):
    return send_file(filename, mimetype='image/gif')

if __name__ == '__main__':
    app.run()
