# Background Remover With Python
This CLI is a background remover for jpg, png, jpeg and webp images. It uses the [rembg](https://github.com/danielgatis/rembg) library for image processing.
## Installation
First you must clone the repository on your machine
```bash
git clone https://github.com/santiago-rincon/background_remover_python.git
```
Once cloned you must enter the project folder, and install all the dependencies 
```bash
pip install -r requirements.txt
```
## Usage
### Remove the background of an image
To remove the background of an image you must specify the path where the image is located (relative or absolute) with the `-i` or `--input` parameter.
By default, the processed image will be stored in the current working directory, if you want to store it in a different location you must specify the path (absolute or relative) with the `-o` or `--output` parameter. In this path you can specify folders that do not exist, the CLI will create it. If the specified path does not end in *".png"* everything will be assumed as a folder and the image will be saved in the last created folder with the original name of the image.

```bash
python background_remover.py -i example.png
```

```bash
python background_remover.py -i ./folder/other_folder/example.png -o C:\User\User\Desktop\final.png
```

```bash
python background_remover.py --input C:\User\user\Pictures\example.png --output ../../final.png
```
### Remove background from multiple images
To remove the background of multiple images you must specify the path to the **FOLDER** (do not include extensions, otherwise it will process only one image) where all the images you want to process are located (relatively or absolutely) with the `-i` or `--input` parameter.
By default, the processed images will be stored in the current working directory, if you want to store them in a different place you should specify the path (absolute or relative) with the `-o` or `--output` parameter. In this path you can specify folders that do not exist, the CLI will create it. If the specified path ends in *".png"* a directory with that name will be created.

```bash
python background_remover.py -i ./folder
```

```bash
python background_remover.py -i ./folder/other_folder/ -o C:\User\User\Desktop\new_images
```

```bash
python background_remover.py --input C:\User\user\Pictures --output ../../new_images
```
## Note for Windows
If you want to add the script to the PATH in windows you must add the text string ".py" to the `PATHEXT` environment variable.

```powershell
$env:PATHEXT += ";.py"
```