from math import floor, ceil
from pathlib import Path
from random import randint
from astropy.utils.shapes import IncompatibleShapeError
from matplotlib.widgets import Slider

import os
import numpy as np
import pandas as pd
from shutil import copy

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider

from astropy.constants import c as C
from astropy.modeling import models, fitting
from astropy import units as u

try:
    from astropy.cosmology import Planck18 as planck
except:
    from astropy.cosmology import Planck15 as planck

# Set the options here

# In the WWT viewer at http://projects.wwtambassadors.org/galaxy-history-universe/,
# zooming in/out makes the size ~90% of what it was before
# So I went for Gaussian noise, with sigma = 10% of the height (in arcmin) for each value

# Without having used the redshift selector, I made my best estimate for a fixed uncertainty there
# so this is Gaussian noise with a fixed sigma

# Tuple options are (min, max)
OPTIONS = {
    'output_dir' : os.path.join(str(Path(__file__).parent), "output"),
    'n_classes': 50,
    'decimal_places': 2,
    'n_students': (20, 30),
    'n_per_student': (4, 5),
    'bin_width': 1,
    'arcmin_frac_noise': 0.1,
    'redshift_sigma': 0.0004,  #From pg 7: https://home.strw.leidenuniv.nl/~franx/technicalresearchinformation/AstronomicalSpectroscopy.pdf  Assuming "moderate" resolution (R=lambda/delta lambda=2500)
}

DATAFILE = os.path.join(str(Path(__file__).parent.parent), "galaxy_data.csv")

# Constants
# L_MW = (100000 * u.lightyear).to(u.Mpc)

# Pat's update: From text exchange with galaxy expert Alice Shapley:
# --Nearby galaxy sizes are usually defined using D_25 - the isophote at which the surface brightness in some band 
#   (like B-band) is 25 mag/arcsec^2
# --As observed from elsewhere, using the D_25 criterion, you would only be able to detect the MW's extent out to
#   ~67,000 light years, so it would make sense to use this distance instead of 100,000 ly.
# --She isn't 100% sure of the 67k ly limit and will help with a more detailed calculation later.
# --Galaxy extents are defined differently for distant galaxies (commonly used is "half-light radius"), 
#   so it's possible the extent should be even smaller (~40-50k ly), but let's stick with this for now
L_MW = (67000 * u.lightyear).to(u.Mpc)
H0 = 70 # km/s/Mpc

# Convenience functions
def mask(df, f):
    return df[f(df)]

def read_galaxy_data(filename):
    return pd.read_csv(filename, converters={'identifier': str.rstrip, 'typ': str.strip})

# Conversions
def redshift_to_velocity(z, relativistic=False):
    if relativistic:
        x = (1+z)**2
        v = C.value * (x-1) / (x+1)
    else:
        v = z * C.value
    return v / 1000 # m -> km

# We use small angle approximation here
def arcmin_to_distance(arcmin):
    rads = arcmin * u.arcmin.to(u.rad)
    dist = L_MW / rads
    return dist.value

def distance_to_arcmin(dist):
    dist_mpc = dist * u.Mpc
    rads = L_MW / dist_mpc
    arcmin = rads * u.rad.to(u.arcmin)
    return arcmin.value

def add_percentage_noise(values, fraction):
    noise = np.random.normal(0, 1, len(values))
    return [ x + n * x * fraction for x,n in zip(values, noise) ]

def add_fixed_noise(values, sigma):
    noise = np.random.normal(0, sigma, len(values))
    return [ x + n for x,n in zip(values, noise) ]

def new_model():
    return models.Linear1D(intercept=0, fixed={'intercept':True})

def age_in_gyr(H0):
     age = planck.clone(H0=H0).age(0)
     unit = age.unit
     return age.value * unit.to(u.Gyr)

def bin_data(data, binning_column):
    binned = data.groupby([binning_column])
    return binned

def export_data(data, filepath):
    data.to_csv(filepath,
        sep=",",
        header=list(data.columns),
        index=False)

def simulate_class(options, export=True, show=False):
    galaxy_data = options['galaxy_data']

    # Number of students, and values per student
    ns = options['n_students']
    nper = options['n_per_student']

    # The first student ID #
    first_id = options.get('last_student_id', 0) + 1

    # Sample the data
    # It's obviously fine if multiple students look at the same galaxy
    # But within each sample of size nper, we want there to be no repeats
    # We then just concatenate these together to make the calculations easier
    sample = pd.concat([ galaxy_data.sample(nper) for _ in range(ns) ])

    # Select a random sample, with some noise
    # Pat's update: Use the measured angular size of the galaxies from the catalog. 
    nd = options['decimal_places']
    arcmin_sample = sample["Ang_maj_amin"]
    arcmin_sample = add_percentage_noise(arcmin_sample, options['arcmin_frac_noise'])
    distance_sample = np.round([ arcmin_to_distance(x) for x in arcmin_sample ], nd)
    redshift_sample = add_fixed_noise(sample["redshift"], options['redshift_sigma'])
    velocity_sample = np.round([ redshift_to_velocity(x, relativistic=False) for x in redshift_sample ], nd)

    # Put the students' data into a DataFrame
    # and bin by student number
    student_range = list(range(first_id, first_id+ns))
    student_data = pd.DataFrame({
        'student_id' : sum([[i]*nper for i in student_range], []),
        'velocity' : velocity_sample,
        'distance' : distance_sample,
        'type' : sample["typ"]
    })
    binned = bin_data(student_data, 'student_id')

    fit = fitting.LinearLSQFitter()
    hubbles = []
    for i in student_range:
        d = binned.get_group(i)
        hubbles.append(np.round(fit(new_model(), d['distance'], d['velocity']).slope.value, nd))
    ages = np.round([ age_in_gyr(H0) for H0 in hubbles ], nd)
    bin_width = options['bin_width']
    minh, maxh = min(hubbles), max(hubbles)
    nbins = ceil(maxh/bin_width) - floor(minh/bin_width)

    overall_fit = fit(new_model(), distance_sample, velocity_sample)
    overall_H0 = round(overall_fit.slope.value, nd)
    overall_age = round(age_in_gyr(overall_H0), nd)

    # Export the data to csv files
    # Maybe we want a different frame?
    if export:
        output_dir = options['output_dir']
        class_id = options['class_id']
        class_summary = pd.DataFrame({
            "student_id" : student_range,
            "class_id": [class_id] * ns,
            "H0" : hubbles,
            "age" : ages,
            "n_measurements": [nper] * ns,
        })
        export_data(class_summary, os.path.join(output_dir, "HubbleSummary_Class_%d.csv" % class_id))
        export_data(student_data, os.path.join(output_dir, "HubbleData_Class_%d.csv" % class_id))

    if show:
        gs = gridspec.GridSpec(4,4, hspace=2, wspace=2)
        plt.tight_layout(pad=0.3)
        
        ax1 = plt.subplot(gs[:2,:2])
        ax1.hist(hubbles, bins=nbins)
        ax1.axvline(overall_H0, color='k', linestyle='solid', linewidth='3') # Pat update: show Hubble estimate from class instead of accepted value
        ax1.set_title("Students' individual H0 values")
        ax1.set_xlabel("H0 (km/s/Mpc)")
        ax1.set_ylabel("No. students")

        ax2 = plt.subplot(gs[:2,2:])
        ax2.scatter(distance_sample, velocity_sample)
        ax2.plot(distance_sample, overall_fit(distance_sample))
        ax2.set_title(f"Best fit: {overall_H0}*d")
        ax2.set_xlabel("Distance")
        ax2.set_ylabel("Velocity")

        ax3 = plt.subplot(gs[2:,1:3])
        ax3.hist(ages, bins=nbins)
        ax3.axvline(overall_age, color='k', linestyle='solid', linewidth='3') # Pat update: show Hubble estimate from class instead of accepted value
        ax3.set_title("Students' individual age values")
        ax3.set_xlabel("Age (Gyr)")
        ax3.set_ylabel("No. students")

        plt.show()

    return student_data, class_summary, overall_H0, overall_age
    

def main(options):

    # Load the galaxy data
    galaxy_data = read_galaxy_data(DATAFILE)

    # Do any filtering that we want to do
    # i.e., do we only want spiral galaxies?
    pd.DataFrame.mask = mask
    galaxy_data = galaxy_data.mask(lambda x: x['MorphType'].isin(['E','Sa','Sb']))
    options['galaxy_data'] = galaxy_data

    # Data columns
    measurement_columns = ['student_id', 'distance', 'velocity']
    student_columns = ['student_id', 'class_id', 'H0', 'age', 'n_measurements']
    class_columns = ['class_id', 'H0', 'age', 'n_students']

    # Containers for data
    # This is vaguely what I imagine the data setup will look like
    # Basically, three levels - individual measurements, student summary, and class summary
    # With the IDs allowing us to connect these in whatever way makes most sense
    # based on the database type
    measurement_data = pd.DataFrame(columns=measurement_columns)
    student_data = pd.DataFrame(columns=student_columns)
    class_data = pd.DataFrame(columns=class_columns)

    # Global options
    n_classes = options['n_classes']
    ns_min, ns_max = options['n_students']
    nper_min, nper_max = options['n_per_student']
    output_dir = options['output_dir']

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    class_options = options.copy()
    class_options['last_student_id'] = 0
    for class_id in range(1, n_classes+1):
        ns = randint(ns_min, ns_max)
        nper = randint(nper_min, nper_max)
        class_options['n_students'] = ns
        class_options['n_per_student'] = nper
        class_options['class_id'] = class_id
        measurements, student_summary, class_H0, class_age = simulate_class(class_options, export=True, show=False)
        class_options['last_student_id'] += ns

        measurement_data = pd.concat([measurement_data, measurements])
        student_data = pd.concat([student_data, student_summary])
        class_data = class_data.append({'class_id': class_id, 'H0' : class_H0, 'age': class_age, 'n_students' : ns}, ignore_index=True)

    copy(os.path.join(output_dir, "HubbleData_Class_1.csv"), os.path.join(output_dir, "HubbleData_ClassSample.csv"))
    copy(os.path.join(output_dir, "HubbleSummary_Class_1.csv"), os.path.join(output_dir, "HubbleSummary_ClassSample.csv"))

    class_data['class_id'] = class_data['class_id'].astype(int)
    export_data(measurement_data, os.path.join(output_dir, "HubbleData_All.csv"))
    export_data(student_data, os.path.join(output_dir, "HubbleSummary_Students.csv"))
    export_data(class_data, os.path.join(output_dir, "HubbleSummary_Classes.csv"))

    students_by_class = student_data.groupby(['class_id'])

    # Get the global H0 and age
    nd = options['decimal_places']
    fit = fitting.LinearLSQFitter()
    distances = measurement_data['distance']
    velocities = measurement_data['velocity']
    global_H0 = round(fit(new_model(), distances, velocities).slope.value, nd)
    global_age = round(age_in_gyr(global_H0), nd)

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.25)
    plt.axvline(global_age, color='k', linestyle='solid', linewidth=3)
    ax.margins(x=0)

    theme_all = { 'color': '#e6e600', 'alpha': 0.5 }
    theme = { 'color' : "#1f77b4", 'alpha' : 0.5 }

    data_all = class_data['age']
    n = ceil((data_all.max() - data_all.min()) / options['bin_width'])
    ax.hist(class_data['age'], bins=n, **theme_all)

    data = students_by_class.get_group(1)['age']
    n = ceil((data.max() - data.min()) / options['bin_width'])
    *_, patches = ax.hist(data, bins=n, **theme)
    ax.set_xlabel("Age (Gyr)")
    ax.set_ylabel("No. students")

    slider = Slider(
        ax      = plt.axes([0.25, 0.1, 0.5, 0.03]),
        label   = "Class ID",
        valmin  = 1,
        valmax  = n_classes,
        valinit = 1,
        valstep = 1
    )

    def update(class_id):
        nonlocal patches
        for p in patches:
            p.remove()
        data = students_by_class.get_group(class_id)['age']
        n = ceil((data.max() - data.min()) / options['bin_width'])
        *_, patches = ax.hist(data, bins=n, **theme)
        fig.canvas.draw_idle()

    slider.on_changed(update)

    plt.show()


if __name__ == "__main__":
    main(OPTIONS)
