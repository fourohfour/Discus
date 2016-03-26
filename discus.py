from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from flask.ext.wtf import Form
from wtforms import SelectMultipleField
from wtforms.validators import DataRequired
from wtforms import widgets
import config
import librarymanager
import os
import ntpath

app = Flask(__name__)
app.config.from_object(config)
app.debug = True

mapping = {}

# class AlbumWidget:
#     def __init__(self):
#         self.widget = widgets.ListWidget(prefix_label=False);
#         self.option_widget = widgets.CheckboxInput();

#     def __call__(self, field, **kwargs):
#         if "_Option" in str(type(field)):
#             print(field.id)
#             opstring = self.option_widget(field, kwargs)
#            ## return widgets.HTMLString("<div >")
#         return widgets.HTMLString("    ")

class CheckboxOverride(widgets.CheckboxInput):
    def __init__(self):
        self.colours = ["PowderBlue","#C2DFFF"]
        self.tick    = 0
        super(CheckboxOverride, self).__init__()

    def __call__(self, field, **kwargs):
        global mapping

        basestr = super(CheckboxOverride, self).__call__(field, **kwargs)
        album = mapping[field.object_data]
        imgstr  = "<div class = 'albumart' style='background-image: url(" + url_for(endpoint = 'library_image', filename = album.art) + ");background-size: 100px 100px;'><div class='checkmark'>✓</div></div>"
        label = [s + ">" for s in field.label().split(">") if s != ""]
        label[1] = "<div class='optiontext boldtext'>" + label[1] + "<br><span class='maintext'>" + album.year + "</span></div>"
        label.insert(1, imgstr)
        labelstr = "".join(label)

        basestr = "<div class='maintext optionbox' style='background-color:" + self.colours[self.tick % 2] + ";'>" + basestr + labelstr + "</div>"
        self.tick += 1
        return basestr

class MultiCheckboxField(SelectMultipleField):
    option_widget =  CheckboxOverride()


class AlbumSelectionForm(Form):
    potential_albums = MultiCheckboxField("Albums")


@app.route('/library/<path:filename>')
def library_image(filename):
    return send_from_directory(os.path.dirname(filename), filename = ntpath.basename(filename), as_attachment= True)


@app.route('/', methods=["GET", "POST"])
def main():
    global mapping
    form = AlbumSelectionForm(request.form)
    lib = librarymanager.Library(".\\library")
    mapping = lib.getAlbums()
    choices = []

    for key in mapping:
        choices.append((key, mapping[key].title + " by " + mapping[key].artist))

    form.potential_albums.choices = choices

    if request.method == "POST":
        status = lib.loadAlbums([int(a) for a in request.form.getlist('potential_albums')],'E:')
        return jsonify({'status' : status})

    print(mapping)

    return render_template('discus.html',
                           title='Discus',
                           form = form,
                           albums = mapping
                          )

if __name__ == '__main__':
    app.run()
