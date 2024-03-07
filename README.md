# Image cropper

Images from the input directory will crop on top and bottom and be saved to
the output directory, according to the `config.ini` file.

## Installing

Step 1. Install [python](python.org)
Step 2. Open the application's directory in a terminal or command line.
Step 3. To install requirements, run this command: `pip install -r requirements.txt`

## Usage

### Using as an application

1. You can simply run program by the command `python path\to\project\directory\main.py` for `windows`,
        and `python3 path\to\project\directory\main.py` for `Linux` or `MacOs`.<br>
        Then you will see text interface with text fields for all necessarry data.

2. You can add additional `arguments` while running program.<br>
   - Arguments will separate by: `existing paths`, `digint`, and `other text`.<br>
   - First `existing path` will use as `directory with uncropped images`;<br>
   - Second `existing path` will use as `directory for save cropped images`;<br>
   - First `digit` will use as `number of pixels for crop`;<br>
   - First `other text` will use as `first part of new file names`;<br>
   - All next `other text` will use as `extentions of files` you want to crop.<br>
   `All arguments that are not included in this list will be ignored.`<br>

3. Copy 'config.ini' from program directory into working directory,
        and edit `config.ini` as you need to.

### Using as a third-party module

First of all, run `pip install -r requirements.txt` in the module's directory to install requirements.

Then you can use the module just like in the `test.py` example file.
