import torch
from torchvision import transforms
from PIL import Image, ImageEnhance
from resnet import resnet50
from deepdream import dream
import numpy as np
import torch
from torch.autograd import Variable
from torchvision import transforms
import os
from resnet import resnet50
from deepdream import dream
from PIL import Image
from util import showtensor
import paramiko
import scp
import paramiko
from paramiko import SSHClient
from scp import SCPClient
import yaml
from time import sleep

DELAY = 10




def remote_connection():
	import paramiko
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh.connect('localhost', username='llaureote', password='')
	except paramiko.SSHException:
		print("Connection Failed")
		quit()

	scp = SCPClient(ssh.get_transport())
	return scp, ssh 


from flask import Flask
app = Flask(__name__)


# load model
model = resnet50(pretrained=True)
if torch.cuda.is_available():
		model = model.cuda()
for param in model.parameters():
		param.requires_grad = False



def yaml_to_dico(yamlpath):
	stream = open(yamlpath, "r")
	#folder = start_yaml_path.replace("conf.yaml","")
	docs = yaml.load_all(stream)
	for doc in docs:
		for k,v in doc.items():
			if k.count('duration') > 0:
			    duration = int(v)*60
			    print(duration)
	
			if k.count('interval'):
				interval = int(v)			
				print(interval)
	parameters = {'duration': duration, 'interval':interval}
	return parameters 

def process(path):
	img_transform = transforms.Compose([
		transforms.ToTensor(),
		transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
			])
	input_img = Image.open(path)
	#input_img = Image.open('./algues.jpg')
	input_tensor = img_transform(input_img).unsqueeze(0)
	input_np = input_tensor.numpy()
	dream(model, input_np)
	

@app.route('/<start_yaml_path>')
def process_image_(start_yaml_path=None):
	start_yaml_path = start_yaml_path.replace(',','/')
	count = 0
	scp = remote_connection()
	yaml_conf = scp[0].get(start_yaml_path, 'tmp_conf.yaml')
	parameters = yaml_to_dico('tmp_conf.yaml')
	target_file = divmod(parameters["duration"], parameters['interval'])[0]
	folder = start_yaml_path.replace('conf.yaml','')
	target_file= 7
	while True :
		sleep(parameters[duration]-DELAY)
		res   = scp[1].exec_command("ls " + folder+'exp'+str(count)+'/captures/0001/') 
		target_file = res[1].read().split(b'\n')[-2]
		target_file = target_file.decode("utf-8") 
		print(target_file)
		scp[0].get(folder+'exp'+str(count)+'/captures/0001/'+target_file)
		#process(target_file)
		count +=1
		from PIL import Image
		import PIL.ImageOps    
		image = Image.open(target_file).convert('L')
		inverted_image = PIL.ImageOps.invert(image)
		converter = PIL.ImageEnhance.Contrast(inverted_image)
		inverted_image = converter.enhance(20)
		inverted_image.save('output.jpg')
		#scp[0].put('output.jpg', folder+'exp'+str(count)+'/output.jpg')      		
		  
		
  
if __name__ == "__main__":
	#yaml_to_dico('conf.yaml')
	app.run()
