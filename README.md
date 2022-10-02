# nafion_swelling
A 1D model of a Nafion thin film with absorption/desorption kinetics, water diffusion, and swelling.

## Objective
Nafion is a common ionomer used in proton exchange membrane fuel cells (PEMFCs). In PEMFC cathode
catalyst layers (CCLs), transport of protons, oxygen, and water through Nafion thin films limit cell
performance. To further our understanding of these transport losses, and to provide insight into
mitigation strategies, physics-based models are a useful tool. Accurate modeling however requires
material-specific properties and species-specific transport parameters that are not necessarily
easy to quantify. Here, we focus on determining kinetic rate constants and diffusion for water
absorption/desorption and transport through Nafion thin films.

This repository provides a 1D model of a Nafion thin film on a solid substrate with its surface
exposed to a constant temperature, pressure, and composition gas phase. The model simulates 
experiments that were performed at Colorado School of Mines, where a quartz crystal microbalance (QCM)
was used to provide high-time-resolution data (~100-200 points per second) for changes in thin-film 
Nafion mass as water moved into and out of a Nafion thin film. The test rig is illustrated in
the figure below. A custom-made flow cap allows for a flow of either dry or humidified nitrogen
gas across Nafion thin films loaded into the QCM. A thermal environment was constructed and placed
around the experimental setup to ensure condensation did not occur, and to test samples at 
temperatures relavent to PEMFCs. Experiments were performed at multiple conditions, with varying
temperatures and relative humidities.

The physics in this model are well understood and are not particularly complicated; however, two 
unknown parameters are present in the model (i.e. the kinetic rate constant for the absorption/desorption
reaction and the diffusion coefficient of water). By using these two values as fitting parameters
and minimizing the error between the model's outputs at conditions that match each experiment,
we provide values that are useful for more complex whole-device PEMFC models.

## Modeling Domain

## Example Outputs

## Simulation Method
This model uses a finite volume method in order to conserve mass within the system. 
An ODE integrator is used along with transient differential equations to evolve the
state of the system until the end of a user-specified simulation time. 

## Installation Instructions
1. Install [Anaconda](https://www.anaconda.com/distribution/) - make sure to get 
Python 3 syntax.
2. Launch "Anaconda Prompt" once the installation has finished.
3. Type `conda create --name echem --channel cantera/label/dev cantera numpy scipy pandas matplotlib` 
into the terminal of "Anaconda Prompt" to set up an environment named "echem" with the 
needed packages.
4. When prompted, type `y` and press enter to finish setting up the environment. 
Agree to any required pop-up messages.
5. Test the new environment by typing `conda activate echem` followed by the enter key.
6. Install an editor for Python files. A good option is [Atom](https://atom.io/).
6. Download all of the files from this repository onto your local machine.
7. Follow the operating instructions below to edit and run the model.

## Operating Instructions
1. Download the files from this respository and save them to your local computer.
2. Open "Anaconda Prompt" and type `conda activate echem` followed by the enter key.
3. Use `cd` to change into the directory where all of the repository files were 
downloaded to.
4. Once inside the correct directory, run the model by typing in `main.py` 
and pressing enter.
5. To edit any of the model inputs or options, open the "main.py" file in any 
Python editor (e.g. Atom).
6. After making any desired changes to "main.py", save the file and repeat 
steps 1-3 to rerun the model.

Optional: If you would prefer to use a developer environment (sort of like Matlab) 
instead of the "Anaconda Prompt" terminal, then do the following: open "Anaconda Navigator", 
select "echem" from the dropdown menu labeled "Applications on" near the top of the page, 
and install "spyder" from the tiles on the screen. Once Spyder is installed, the 
"main.py" file can be opened within the program, where it can be both edited and 
run without the need for a separate editor and terminal. For more details visit Spyder's 
website [here](https://www.spyder-ide.org/).

Note: The "optimize.py" file demonstrates another method that can be used to run this model. 
Instead of running the "main.py" file directly, you can import the `simulation` class into 
another script. After creating an instance of this class, you can execute the `exp_deets` method 
to set any of experimental details. For a full list of input options (and descriptions of
each), use the `help_dict` method build into the class.

## License
This tool is released under the BSD-3 clause license, see LICENSE for details.

## Citing the Model
This model is versioned using Zenodo:

If you use this tool as part of a scholarly work, please cite using:

> C. R. Randall and S. C. DeCaluwe. (2022) Nafion Swelling v1.0 [software]. Zenodo.

A BibTeX entry for LaTeX users is

```TeX
@misc{Nafion-Swelling,
    author = {Corey R. Randall and Steven C. DeCaluwe},
    year = 2022,
    title = {Nafion Swelling v1.0},
    doi = {},
    url = {https://github.com/c-randall/nafion_swelling},
}
```

In both cases, please update the entry with the version used. The DOI for the latest 
version is given in the badge at the top, or alternately <> will
take you to the latest version (and generally represents all versions).
