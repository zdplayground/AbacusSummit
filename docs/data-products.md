# Data Products

## Overview

We have designed a set of data products aimed at supporting mock
catalogs to be constructed using halo occupation distributions, as
well as efficient access to measurements of the density fields.
Minimization of data volume has been a high priority.  Indeed, we
have stored full particle snapshots only for a few simulations.
Even with this economy, we are producing 2 PB of data products.

The key data products are:
1) Halo catalogs with various statistics computed on-the-fly
from the full particle set.
2) 10% subsamples of particles, consistently selected across redshift,
output with position, velocity, kernel density, and particle ID,
organized so as to preserve halo membership.
3) A light cone stretching from the corner of the box and including
a single second periodic copy of the box.  This provides an octant of
sky to z=0.8 and about 800 sq deg to z=2.4.  The outputs are the 
subsample of particles, as well as the Nside=16384 healpix pixel 
number for all particles.  
4) Full particle catalogs for a few timeslices of a few boxes.

We perform group finding at 12 primary redshifts and 24 secondary
redshifts.  The primary set is z=0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 1.1, 
1.4, 1.7, 2.0, 2.5, and 3.0, and this will be where most users
should focus.

At each primary redshift, we output the properties computed for the
L1 halos in `halo_info` files.  The list of properties is below.

We also output a subsample of the particle, split into 3% and 7%
sets (so 10% total), called A and B, so that users can minimize
their data access depending on application.  These subsamples are
consistent across redshift and are selected based on a hash of the
particle id number, so effectively randomly.

The particles are further split into files based on whether the
particle is in a L0 halo or not.  The particles belonging to a given
L1 halo are contiguous in each of the A and B files, and the start
and number of the two sets are in in the `halo_info` files.  This
allows a user to easily fetch a random subsample of particles from
the L1 halo; we use these for satellite galaxy positions.

Particle positions and velocities are output in one file.  A separate
file contains the unique particle id number, which is easily parsed
as the initial grid position, as well as the kernel density estimate
and a sticky bit that is set if the particle has ever been in the most
massive L2 halo of a L1 halo with more than 35 particles.

Hence, each primary redshift yields 9 set of files: `halo_info` and then
{A,B} x {field,halo} x {RV,PID}.

Each set of files is split into 34 files, containing 50 slabs each 
(51 for the last), to permit users to work on portions of the
simulation.  

A potential confusing aspect is that field particles are assigned
to a file based on the slab number of their cell, but halo particles
are assigned to a file based on the slab number of their L0 halo.
L0 halos can span up to 20 slabs (though most are much smaller, as
a slab is just over 1 Mpc wide) and can involve hundreds of cells.
A L0 halo is assigned to a slab based on the lowest x-value of its
cells.  In other words, if a halo has particles from slabs C..D,
it will be in the file for slab C.  So one cannot simply take the
halo and field files of matching slab range and get the union of
all particles.


For the 24 secondary redshifts, we output the halo catalogs and the 
halo subsample particle IDs (w/densities and sticky L2 tag) only, 
so not the positions/velocities nor the field particles.  

The purpose of the secondary redshifts is to support generation 
of merger trees, as the PIDs can be used to associate halos between
snapshots.  It may also be possible to use the finer redshift sampling
to associate halo catalogs to the light cones, as the subsample of 
particles are the same.  For example, one could use the halo catalog
to generate a HOD at a redshift, assign a given PID to be a satellite
galaxy, then go find that PID in the light cone files.

## Halo Statistics

Here we list the statistics computed for each halo.

* `uint64_t id`: A unique halo number.

* `uint64_t npstartA`: Where to start counting in the particle output for subsample A

* `uint64_t npstartB`: Where to start counting in the particle output for subsample B

* `uint32_t npoutA`: Number of taggable particles pos/vel/aux written out in subsample A

* `uint32_t npoutB`: Number of taggable particles pos/vel/aux written out in subsample B

* `uint32_t ntaggedA`: Number of tagged particle PIDs written out in subsample A. A particle is tagged if it is taggable and is in the largest L2 halo for a given L1 halo. 

* `uint32_t ntaggedB`; 

* `uint32_t N`: The number of particles in this halo

* `uint32_t L2_N[N_LARGEST_SUBHALOS]`: The number of particles in the largest L2 subhalos

* `uint32_t L0_N`: The number of particles in the L0 parent group

* `float SO_central_particle[3]`: Coordinates of the SO central particle

* `float SO_central_density`: Density of the SO central particle. 

* `float SO_radius`: Radius of SO halo (distance to particle furthest from central particle) 

* `float SO_L2max_central_particle[3]`: Coordinates of the SO central particle for the largest L2 subhalo. 

* `float SO_L2max_central_density`: Density of the SO central particle of the largest L2 subhalo. 

* `float SO_L2max_radius`: Radius of SO halo (distance to particle furthest from central particle) for the largest L2 subhalo


The following quantities are computed using a center defined by 
the center of mass position and velocity of the largest L2 subhalo.
In addition, the same quantities with `_com` use a center defined
by the center of mass position and velocity of the full L1 halo.

All second moments and mean speeds are computed only using
particles in the inner 90% of the mass relative to this center.

* `float x_L2com[3]`: Center of mass pos of the largest L2 subhalo

* `float v_L2com[3]`: Center of mass vel of the largest L2 subhalo

* `float sigmav3d_L2com`: Sum of eigenvalues

* `float meanSpeed_L2com`: Mean speed

* `float sigmav3d_r50_L2com`: Velocity dispersion of the inner 50% of particles

* `float meanSpeed_r50_L2com`: Mean speed of the inner 50% of particles

* `float r100_L2com`: Radius of 100% of mass, relative to L2 center. 

* `float vcirc_max_L2com`: max circular velocity, based on the particles in this L1 halo 

* `int16_t sigmavMin_to_sigmav3d_L2com`: Min(sigmav_eigenvalue) / sigmav3d, compressed

* `int16_t sigmavMax_to_sigmav3d_L2com`: Max(sigmav_eigenvalue) / sigmav3d, compressed

* `uint16_t sigmav_eigenvecs_L2com`: Eigenvectors of the velocity dispersion tensor, compressed into 16 bits. 

* `int16_t sigmavrad_to_sigmav3d_L2com`: sigmav_rad / sigmav3d, compressed

* `int16_t sigmavtan_to_sigmav3d_L2com`: sigmav_tan / sigmav3d, compressed

* `int16_t r10_L2com`, `r25_L2com`, `r33_L2com`, `r50_L2com`, `r67_L2com`, `r75_L2com`, `r90_L2com`, `r95_L2com`, `r98_L2com`: Radii of this percentage of mass, relative to L2 center. Expressed as ratios of r100 and compressed to int16. 

* `int16_t sigmar_L2com[3]`: The eigenvalues of the moment of inertia tensor

* `int16_t sigman_L2com[3]`: The eigenvalues of the weighted moment of inertia tensor, in which we have computed the mean square of the normal vector between the COM and each particle.

* `uint16_t sigmar_eigenvecs_L2com`: The eigenvectors of the inertia tensor, compressed

* `uint16_t sigman_eigenvecs_L2com`: The eigenvectors of the weighted inertia tensor, compressed

* `int16_t rvcirc_max_L2com`: radius of max circular velocity, stored as ratio to r100, relative to L2 center

In most cases, these quantities are compressed to save space.  Sometimes this is simple: e.g., when we have the chance to store a ratio in the range [0,1], we
multiply by 32000 and store as an int16.  Others are more complicated, e.g., 
the Euler angles of the eigenvectors are stored to about 4 degree precision and
all packed into an uint16.

We are providing a Python package to undo this compression and expose
Astropy tables (and therefore NumPy arrays) to the user.


## Light Cones

The light cone is structured as three periodic copies of the box,
centered at (0,0,0), (0,0,2000), and (0,2000,0) in Mpc/h units.  This is observed
from the location (-950, -950, -950), i.e., 50 Mpc inside a corner.
This provides an octant to a distance of 1950 Mpc/h (z=0.8), shrinking
to two patches each about 800 square degrees at a distance of 3950 Mpc/h (z=2.4).

The three boxes are output separately and the positions are referred
to the center of each periodic copy, so the particles from the higher
redshift box need to have 2000 Mpc/h added to their z coordinate.

Particles are output from every time step (recall that these
simulations use global time steps for each particle).  In each step,
we linearly interpolate to find the time when the light cone
intersects this each particle, and then linearly update the position
and velocity to this time.

The HealPix pixels are computed using +z as the North Pole, i.e., 
the usual (x,y,z) coordinate system.


## Data Model

Here we describe the data model of the AbacusSummit data products.

The halo statistics are in `halo_info` files.  These are stored as
ASDF files, where each column is in a contiguous binary portion.
The ASDF header is human-readable, meaning one can use a Linux
command line tool like `less` to examine the simulation metadata
stored in every ASDF file.

The particles position and velocities are stored in RV files in a
bit-truncated and compressed format.  What is revealed to the user
is three 32-bit integers, for x, y, and z.  The positions map
[-0.5,0.5] to +-500,000 and are stored in the upper 20 bits.  The
velocites are mapped from [-6000,6000) km/s to [0,4096) and stored
in the lower 12 bits.

The particle id numbers and kernel densities are stored in PID files
packed into a 64-bit integer.  The id numbers are simply the (i,j,k)
index from the initial grid, and these 3 numbers are placed as the
lower three 16-bit integers.  The kernel density is stored as the
square root of the density in cosmic density units in bits 1..12
of the upper 16-bit integer.  Bit 0 is used to mark whether the
particle has ever been inside the largest L2 halo of a L1 halo with
more than 35 particles; this is available to aid in merger tree
construction.

The RV and PID files are then piecewise byte-transposed and zstd
compressed.  We call this trz compression, and provide a utility
(https://github.com/abacusorg/trz).  We have found that transposing
by 12 and 8 bytes respective provides substantially better compression,
as some bytes in each number have much less variation than others,
and the x and y coordinates vary more slowly than z due to the fact
that the particles are output in cell order.  We use [zstd](https://www.zstd.net) as the
compression because it is much faster in decompression than gunzip;
we expect that even a single thread can keep up with the read rate
of a disk array.

CRC32 checksums are provided for all files.  These should match the
GNU `cksum` utility, pre-installed in most Linux environments.
We also offer a fast implementation of `cksum` with about 10x better performance:
https://github.com/abacusorg/fast-cksum.