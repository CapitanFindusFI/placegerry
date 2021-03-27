import io
from flask import Flask, send_file
from search import search_image

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/<width>/<height>')
def search_route(width, height):
    send_image = search_image(width, height)
    image_path = "{}/{}".format("downloaded", send_image)
    print("Sending image: {}".format(image_path))
    return send_file(image_path, attachment_filename = "gerry.jpg", mimetype = "image/jpeg")

@app.route('/')
def empty_route():
    return 'Hello, Gerry'


if __name__ == "__main__":
    app.run()
