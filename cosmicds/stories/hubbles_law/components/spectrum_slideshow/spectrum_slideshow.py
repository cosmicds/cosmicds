import ipyvuetify as v
from pathlib import Path
from traitlets import Int, Bool, Unicode
from cosmicds.utils import load_template


#theme_colors()

class SpectrumSlideshow(v.VuetifyTemplate):
    template = load_template("spectrum_slideshow.vue", __file__, traitlet=True).tag(sync=True)
    step = Int(0).tag(sync=True)
    length = Int(9).tag(sync=True)
    dialog = Bool(False).tag(sync=True)
    currentTitle = Unicode("").tag(sync=True)
    #exploration_complete = Bool(False).tag(sync=True)
    #intro_complete = Bool(False).tag(sync=True)

    _titles = [
        "Light and Spectra",
        "Light and Spectra", 
        "Light and Spectra",
        "Light and Spectra",
        "Doppler Shift",
        "Doppler Shift",
        "Atom & Molecule Emissions",
        "Emission & Absorption"
    ]
    _default_title = "Light and Spectra"
    _default_image1 = str(Path(__file__).parents[1] / "data" / "images" / "refraction_diffraction_spectra.png")

    image_path = str(Path(__file__).parents[1] / "data" / "images" / "")
    print(image_path)



    def __init__(self, *args, **kwargs):
        self.currentTitle = self._default_title
        self.currentImage1 = self._default_image1

        def update_title(change):
            index = change["new"]
            if index in range(len(self._titles)):
                self.currentTitle = self._titles[index]
            else:
                self.currentTitle = self._default_title

        self.observe(update_title, names=["step"])

        super().__init__(*args, **kwargs)


