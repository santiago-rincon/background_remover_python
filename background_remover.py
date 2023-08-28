# Importing standard libraries 
import argparse, os, signal, sys

# Importing third-party libraries
from rembg import remove
from colorama import Fore, init
import pyfiglet

# Initializing colorama for colors in the terminal output
init()

# Global variables
ALLOWED_FORMATS = ('.png', '.jpg', '.jpeg', 'webp')
CONFIRM_OPTIONS = ('yes', 'y')
pwd = os.getcwd()

# Functions
def remove_background(input_p,output,counter=1,total_len=1):
    input_file = os.path.split(input_p)[1]
    if not output.endswith(ALLOWED_FORMATS):
        file = f'{os.path.sep}{input_file}'
        file = f'{os.path.splitext(file)[0]}.png'
        output += file
    if os.path.split(input_p)[0] == os.path.split(output)[0]:
        output = output.replace(input_file,f'out.{input_file}')
    if not os.path.exists(os.path.split(output)[0]):
        os.makedirs(os.path.split(output)[0])
    print(Fore.GREEN + f'[+] Processing images [{counter}/{total_len}]...\r', end='')
    try:
        with open(input_p, 'rb') as i, open(output, 'wb') as o:
            o.write(remove(i.read()))
        if counter == total_len:
            print(Fore.MAGENTA + f'\n[+] Output file: {output}') if counter == 1 else print(Fore.MAGENTA + f'\n[+] Output folder: {os.path.split(output)[0]}')
    except Exception as e:
        print(Fore.GREEN + f'[+] Processing images [{counter}/{total_len}]...')
        print(Fore.RED + f'[-] The image \"{input_file}\" could not be processed\n[-] Error: {str(e)}')
        if counter != total_len:
            confirm = input(Fore.YELLOW + "[!] Do you want to keep trying with the other files? y/[n]: ")
            if not confirm in CONFIRM_OPTIONS:
                print(Fore.MAGENTA + f'\n[+] Output file: {output}') if counter == 1 else print(Fore.MAGENTA + f'\n[+] Output folder: {os.path.split(output)[0]}')
                finish_program()

def absolute_path(path):
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    return path

def confirm_execution(input_path, output_path):
    if not input_path.endswith(ALLOWED_FORMATS) and output_path.endswith(ALLOWED_FORMATS):
        confirm = input(Fore.YELLOW + f"[!] When you specify a folder as input and an image as output, a folder with the name \"{os.path.split(output_path)[1]}\" will be created where all processed images from the folder that was specified as input will be saved.\nDo you want to continue? y/[n]: ")
        confirm = confirm.lower()
        return confirm
    else :
        confirm = "yes"
        return confirm

def change_extension(path):
    if not path.endswith('.png'):
        path = f'{os.path.splitext(path)[0]}.png'
        return path
    else:
        return path

def finish_program():
    print(Fore.RED + "\n[-] Program terminated.")
    sys.exit(1)

def ctrl_c (sig, frame):
    try:
        print(Fore.GREEN + f'[+] Processing images [{counter}/{total_files_len}]...')
    except:
        counter = 1
        total_files_len = 1
        print(Fore.GREEN + f'[+] Processing images [{counter}/{total_files_len}]...')
    print(Fore.YELLOW + "[!] A forced output has occurred, check the output folder to verify the integrity of the processed files. ")
    print(Fore.MAGENTA + f'\n[+] Output folder: {output_path}')
    finish_program()

# Control C 
signal.signal(signal.SIGINT, ctrl_c)

# Banner 
print(Fore.YELLOW + pyfiglet.figlet_format("Background remover"))

# Arguments
parser = argparse.ArgumentParser(prog='Background remover for images',usage=Fore.BLUE + '\npython background_remover.py -i[--input] <example.png> -o[--output] <example_output.png>.\nFor more information:\npython background_remover.py -h[--help]',description=Fore.GREEN + f'This program removes the background from the image, formats allowed: {ALLOWED_FORMATS}' + Fore.YELLOW, epilog=Fore.MAGENTA + '[!] Program create by Cristian Santiago Rincón',)
parser.add_argument('-i', '--input', help = Fore.CYAN + 'Path to the input image. If you do not specify an input image, all images in the current folder will be taken.' + Fore.YELLOW, required = True, type = str, metavar = 'example.png')
parser.add_argument('-o', '--output', help = Fore.CYAN + 'Path to the output image or path to the folder where the output images will be saved. If you do not specify the parameter, the image(s) will be saved in the current working directory. If the path contains a folder that does not exist on the system, it will be created. The output image extension must be \"png\", otherwise it will be changed. If it does not contain an extension it will be considered as a folder.', required = False, default = pwd, type = str, metavar = 'example_output.png')
args = parser.parse_args()
input_path,output_path  = args.input,args.output

# Absolute paths
input_path = absolute_path(input_path)
output_path = absolute_path(output_path)

# Delete last character if it is a quotation mark (Windows)
if output_path[-1] == "\"":
    output_path = output_path[:-1]

# Confirmation when input are a folder and output is an image
if confirm_execution(input_path,output_path) in CONFIRM_OPTIONS: 

    if output_path.endswith(ALLOWED_FORMATS):
        output_path = change_extension(output_path)
        print(Fore.YELLOW + "[!] NOTE: the output image extension has been changed to \"png\".")

    if input_path.endswith(ALLOWED_FORMATS):
        remove_background(input_path,output_path)
    else:
        counter = 1
        try:
            files = os.listdir(input_path)
        except:
            print(Fore.RED + f'[-] An error has occurred, possible causes:\n\t[!] The folder \"{input_path}\" does not exist.\n\t[!] The image \"{input_path}\" does not exist.\n\t[!] The file \"{input_path}\" is not supported for image processing.')
            finish_program()
        total_files = [img for img in files if img.endswith(ALLOWED_FORMATS)]
        total_files_len = len(total_files)
        if total_files_len != 0:
            for file in total_files:
                i = os.path.join(input_path, file)
                o = os.path.join(output_path, file)
                o = change_extension(o)
                remove_background(i,o,counter,total_files_len)
                counter += 1
        else:
            print(Fore.YELLOW + f'[!] The folder \"{input_path}\" does not contain any image.')
else:
    finish_program()