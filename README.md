# Tripleadapt Frontend

For now all the codes are in React.js. The node_mouldes are untracked so please run in reach directory the following command before starting up:

`npm install`


# Tripleadapt CLEVR Interface & Processing

The package clevr contains the data processing received from the CLEVR API from the interface via REST (REST/CLEVR.py). This package includes data processing from the .xml/.bpmn to a readable format
This includes loading/storing data from/into a mongodb, which needs some packages to be installed. Also, for the model, we use the rmm4py. To install all dependencies, go on as follows:

### Clone for development
 0. Requirements: Git, Python > 3.8, Python IDE, Jupyter Notebooks (if not already supported by IDE).
 1. Optional: Create a virtual environment.
 2. Download or clone repository.
 3. Install all dependencies (activate your virtual environment before if you created one):     
     ```pip install -r path/to/requirements.txt```
 
 4. Start working

### Installation for use in other projects
Make sure you have a SSH-key. Via pip run 

```pip install git+ssh://git@gitlab-iwi.dfki.de/rmm4py/rmm4py-core```

which will copy and install the project.
 
---



