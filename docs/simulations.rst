Simulations
===========

This page contains the specification of the simulations in AbacusSummit.  Simulations specifications are given a descriptive label:

* **Base**: this is our standard size, 6912^3 particles in 2 Gpc/h.

* **High**: A box with 6x better mass resolution, 6300^3 in 1 Gpc/h.

* **Highbase**: A 1 Gpc/h box with the base mass resolution.

* **Huge**: these are larger boxes run with 27x worse mass resolution. 

* **Hugebase**: Re-runs of some 2 Gpc/h boxes with the same 27x worse mass resolution.

* **Fixedbase**: Simulations with the base mass resolution but fixed-amplitude initial conditions, 4096^3 in 1.18 Gpc/h.

* **Small**: Simulations with base mass resolution but 1728^3 particles in 0.5 Gpc/h.

Run-time products: 

Only a few of our simulations include the full timeslice output;
we typically output only subsamples.  The full list is z=3.0, 2.5,
2.0, 1.7, 1.4, 1.1, 0.8, 0.5, 0.4, 0.3, 0.2, 0.1.  The partial
list is z = 2.5, 1.4, 0.8, 0.2.  Partial+HiZ adds z=3.0 and 2.0 to that.

Subsamples of particles, with positions, velocities, ID numbers, and kernel density
estimates, are typically provided at the same 12 redshifts as the Full list in the
previous paragraph.  CompaSO group finding is run at these redshifts as well as 21 others.
The huge and hugebase sims have fewer group finding and subsample epochs.

Base sims and Huge sims have light-cone outputs; others do not.

A base simulation typically produces about 10 TB of subsampled output, and 
each output slice is another 4 TB above that.

We ran 2000 small simulations, intended for studies of covariance
matrices in periodic boundary conditions.  These have particle
subsample outputs at z=1.4, 1.1, 0.8, 0.5, and 0.2, as well as halo
finding at all redshifts >0.2.  However, about 15% of these simulations
crashed due to some unresolved issue, almost certainly uncorrelated
with any property of the large-scale structure in the simulation.
Some of the crashed ones still produced usable outputs at higher
redshifts.  We have chosen to present the 1883 that yielded outputs
at z=1.1; 1671 of these reached z=0.2.  The numbering between ph3000
and ph4999 will be irregular.

The cosmologies in the "Cosm" column are tabulated in :doc:`cosmologies`.

-----

Download the simulations table `here <https://github.com/abacusorg/AbacusSummit/blob/master/Simulations/simulations.csv>`_.

.. note:: The following table is wide, you may have to scroll to the right to see all the columns.

.. csv-table::
    :file: ../Simulations/simulations.csv
    :header-rows: 1
    :escape: '
