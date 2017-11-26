from PIL import Image
from io import BytesIO
#from IPython.display import clear_output, Image, display
import numpy as np
import time

def showarray(a, fmt='jpeg'):    
    a = np.uint8(np.clip(a, 0, 255))
    f = BytesIO()
    #img = Image.open(f)
    #PIL.Image.fromarray(a).save(f, fmt)
    #Image(data=f.getvalue()))
    #img.save("a_test.png")
    #print(type(f))
    im = Image.fromarray(a)
    im.save(str(time.time()).replace('.',"")+'.jpeg')

def showtensor(a):
	fmt='jpeg'
	mean = np.array([0.485, 0.456, 0.406]).reshape([1, 1, 3])
	std = np.array([0.229, 0.224, 0.225]).reshape([1, 1, 3])
	inp = a[0, :, :, :]
	inp = inp.transpose(1, 2, 0)
	inp = std * inp + mean
	inp *= 255 
	showarray(inp)
	clear_output(wait=True)
