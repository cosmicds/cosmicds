from math import floor, ceil
from random import randint
from astropy.utils.shapes import IncompatibleShapeError
from matplotlib.widgets import Slider

import os
import csv
import numpy as np
import pandas as pd

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
    'output_dir' : "output",
    'n_classes': 50,
    'decimal_places': 2,
    'n_students': (20, 30),
    'n_per_student': (4, 5),
    'bin_width': 5,
    'arcmin_frac_noise': 0.1,
    'redshift_sigma': 0.0004,  #From pg 7: https://home.strw.leidenuniv.nl/~franx/technicalresearchinformation/AstronomicalSpectroscopy.pdf  Assuming "moderate" resolution (R=lambda/delta lambda=2500)
}

DATAFILE = os.path.join("..", "galaxy_data.csv")

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

def append_to_dict(d, keys, values):
    for k, v in zip(keys, values):
        d[k].append(v)

def export_class_summary(filepath, hubbles, ages):
    if len(hubbles) != len(ages):
        raise ValueError("Hubble constant and age arrays do not have the same length")
    
    ns = len(hubbles)
    with open(filepath, 'w') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["StudentNum", "StudentH0 (km/s/Mpc)", "StudentAge (Gyr)"]) # Headers
        for i in range(ns):
            writer.writerow([i+1, hubbles[i], ages[i]])

def export_class_data(filepath, vel_binned, dist_binned):

    if len(vel_binned) != len(dist_binned):
        raise ValueError("Overall distance and velocity arrays do not have the same length")

    ns = len(vel_binned)
    with open(filepath, 'w') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["StudentNum", "Velocity", "Distance"]) # Headers
        for i in range(ns):
            vs = vel_binned[i]
            ds = dist_binned[i]
            if len(vs) != len(ds):
                raise ValueError("Distance and velocity arrays at index %d do not have the same length" % i)
            np = len(vs)
            for j in range(np):
                writer.writerow([i+1, vs[j], ds[j]])

def export_overall_summary(filepath, classes_data):

    keys = ['class_id', 'H0', 'age', 'n_students']
    with open(filepath, 'w') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(keys) # Headers
        for tpl in zip(*[classes_data[k] for k in keys]):
            writer.writerow(tpl)



def simulate_class(options, export=True, show=False):
    galaxy_data = options['galaxy_data']

    # Number of students, and values per student
    ns = options['n_students']
    nper = options['n_per_student']

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

    # The lambda function just cuts up the list into chunks of size nper
    # Basically just undoing the pd.concat
    binned_by_student = lambda lst: [ lst[nper*i:nper*(i+1)] for i in range(ns) ]
    d_binned = binned_by_student(distance_sample)
    v_binned = binned_by_student(velocity_sample)

    fit = fitting.LinearLSQFitter()
    hubbles = np.round([ fit(new_model(), ds, vs).slope.value for ds,vs in zip(d_binned, v_binned) ], nd)
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
        export_class_summary(os.path.join(output_dir, "HubbleSummary_Class_%d.csv" % class_id), hubbles, ages)
        export_class_data(os.path.join(output_dir, "HubbleData_Class_%d.csv" % class_id), v_binned, d_binned)

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

    return d_binned, v_binned, hubbles, ages, overall_H0, overall_age
    

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
    empty_container = lambda lst: {x: [] for x in lst}

    # Containers for data
    # This is vaguely what I imagine the data setup will look like
    # Basically, three levels - individual measurements, student summary, and class summary
    # With the IDs allowing us to connect these in whatever way makes most sense
    # based on the database type
    measurement_data = empty_container(measurement_columns)
    student_data = empty_container(student_columns)
    class_data = empty_container(class_columns)

    # Global options
    n_classes = options['n_classes']
    ns_min, ns_max = options['n_students']
    nper_min, nper_max = options['n_per_student']
    output_dir = options['output_dir']

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    student_id = 0
    class_options = options.copy()
    for class_id in range(1,n_classes+1):
        ns = randint(ns_min, ns_max)
        nper = randint(nper_min, nper_max)
        class_options['n_students'] = ns
        class_options['n_per_student'] = nper
        class_options['class_id'] = class_id
        db, vb, hubbles, ages, class_H0, class_age = simulate_class(class_options, export=True, show=False)

        for dists, vels, hub, age in zip(db, vb, hubbles, ages):
            student_id += 1
            for d, v in zip(dists, vels):
                append_to_dict(measurement_data, ['student_id', 'distance', 'velocity'], [student_id, d, v])

            append_to_dict(student_data, ['student_id', 'class_id', 'H0', 'age', 'n_measurements'], [student_id, class_id, hub, age, nper])
        
        append_to_dict(class_data, ['class_id', 'H0', 'age', 'n_students'],[class_id, class_H0, class_age, ns])

    export_overall_summary(os.path.join(output_dir, "HubbleSummary_Overall.csv"), class_data)

    measurement_data = pd.DataFrame(measurement_data)
    student_data = pd.DataFrame(student_data)
    class_data = pd.DataFrame(class_data)

    get_class_data = lambda cls_id: student_data[student_data.class_id == cls_id]

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

    data = get_class_data(1)['age']
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
        data = get_class_data(class_id)['age']
        n = ceil((data.max() - data.min()) / options['bin_width'])
        *_, patches = ax.hist(data, bins=n, **theme)
        fig.canvas.draw_idle()

    slider.on_changed(update)

    plt.show()


if __name__ == "__main__":
    main(OPTIONS)
