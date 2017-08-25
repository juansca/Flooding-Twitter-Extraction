# Flooding-Twitter-Extraction
Tool for extracting and processing data related to floods and inundations in Córdoba, Argentina

## Install and uninstall
### Install

You must have anaconda installed in order to install the package and the environment.
Download anaconda from [here](https://www.continuum.io/downloads).

```
conda env create -f environment.yml;
pip install -r requirements.py
```

**Note**: This will create a new environment.

### Uninstall
To uninstall run:

```
conda remove -n FloodTwitExt --all
```


## Importante

Instalar 'wkhtmltopdf' para que funcione la captura de pantalla de las
webpages (usando imgkit).
En Linux:
```
sudo apt-get install wkhtmltopdf
```
