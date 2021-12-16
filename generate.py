'''
The python script generates captcha dataset. The size and length of 
each captcha image are determined by input parameters from the 
use through a data.dat file
'''

from captcha.image import ImageCaptcha
from pathlib import Path
import random  
import string  
import os 


default_path = Path('./data')


def random_string(letter_count:int, digit_count:int,punc_count:int):  
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))  
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))  
    str1 += ''.join((random.choice('%&\.+/,+()<=?:~') for x in range(punc_count)))  
    # str1 += ''.join((random.choice(' ') for x in range(max_string_length - (letter_count+digit_count+punc_count))))
    sam_list = list(str1) 
    random.shuffle(sam_list) 
    final_string = ''.join(sam_list)  
    return final_string  

def generate_captcha_data(params:dict):
	path = params['path']
	dataset_size = params['size']
	img_size     = params['img_size']
	char_size    = params['char_size']
	punc_size    = params['punc_size']

	for i in range(dataset_size):
		image   = ImageCaptcha(width = img_size[0], height = img_size[1])
		str_len = random.randint(1,char_size)
		captcha_text = random_string(str_len,char_size-str_len,punc_size) 
		img_path= os.path.join(path,'{}.png'.format(''.join(i for i in captcha_text if i not in list(string.punctuation) )))
		image.write(captcha_text, img_path)

def load_parameters(path:Path) -> dict:
	FILE = open(path,'r')
	args = {'path':'','size':50000,'img_size':(),'char_size':8,'punc_size':2}
	args_keys = list(args.keys())

	for i,line in enumerate(FILE):
		if i == 0:
			args[args_keys.pop(0)] = Path(line.split('\n')[0])
		elif " " in line:
			args[args_keys.pop(0)] = int(line.split())
		elif "," in line:
			args[args_keys.pop(0)] = (int(line.split(',')[0]),int(line.split(',')[1]))
		else:
			args[args_keys.pop(0)] = int(line)

	return args

def find_parameters() -> bool:
	path = None
	for dirs,_,files in os.walk('.', topdown=True):
		for file in files:		
			if '.dat' in file:
				path = Path(dirs) / file
	return path


def check_path(path:Path) -> None:
	if not path.exists():
		os.mkdir(path)
	else: pass
	return

if __name__ == '__main__':
	args_file = find_parameters()
	args      = load_parameters(args_file)

	if not args['path'] == '':
		check_path(args['path'])
	else:
		check_path(default_path)

	generate_captcha_data(args)
