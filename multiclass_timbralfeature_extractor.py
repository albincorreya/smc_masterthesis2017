#==========================================
'''
Python script to extract timbral attributes from audiocommons timbral models
from the specified dataset and store it as a JSON file for every sound classes.


Albin Andrew Correya
Music Technology Group
UPF
'''
#==========================================


# import neccessary packages
from essentia.standard import *
import essentia.standard as estd
import Timbral_Brightness as bright
import Timbral_Roughness as rough 
import Timbral_Depth as depth
import Timbral_Hardness as hard
import pandas as pd 
import os, json, csv 

from progressbar import ProgressBar
pbar = ProgressBar()


def normaliseListRange(myList):
	'''
	Function to normalise the elements in a list to the range (0,100)

	 Normalize to [0, 1]:
	 m = min(array);
	 range = max(array) - m;
	 array = (array - m) / range;

	Then scale to [x,y]:
	range2 = y - x;
	 normalized = (array*range2) + x;
	'''
	norm_list = list()
	ranges = max(myList) - min(myList)
	for element in myList:
		var = (element - min(myList))/ranges # normalise to the range (0,1)
		var  = var * 100
		norm_list.append(var)
	return norm_list



def parseToJson(ids,names,b,r,h,d,cname):
	main_dict = dict()
	for val in zip(ids,names,b,r,h,d):
		#print 'Value --->',val
		sdict = dict()
		fdict = dict()
		sdict['sound_name'] = val[1] 
		sdict['brightness'] = val[2]
		sdict['roughness'] = val[3]
		sdict['hardness'] = val[4]
		sdict['depth'] = val[5]
		main_dict[val[0]] = sdict
	with open(cname+".json","w") as data:
		json.dump(main_dict,data)
	return 


# replace it with your dataset file directory
path = '/Users/Correya/desktop/Master_Thesis/freesound_dataset/client_download_freesound/100_fs_dataset/'


folders = os.listdir(path)
if '.DS_Store' in folders:    #remove the hidden file in the folders in mac osx
	folders.remove('.DS_Store')
if 'Explosion' and 'Gunshot' in folders:
	folders.remove('Explosion')
	folders.remove('Gunshot')



for folder in pbar(folders):
	feature_dict = dict()
	ignore_list = list()
	b = list()
	r = list()
	h = list()
	d = list()
	ids = list()
	names = list()
	class_name = list()
	files = os.listdir(path+folder)
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	i = 1
	print "\nStart computing features for the class >>", folder
	for sound in files:
		if not sound.endswith('.mp3') or sound.endswith('.ogg'):
			print '\n-------- '+str(i)+' -----------'
			str_sound = sound.split('__')
			#print '\nSPLIT',str_sound
			sound_id = str_sound[0]
			sound_name = str_sound[1]
			print '\nComputing feature for sound >>',sound
			fname = path + folder + '/' + sound
			try:
				brightness = bright.timbral_brightness(fname)
				print '.......brightness done'
				roughness = rough.timbral_roughness(fname)
				print '........roughness done'
				hardness = hard.timbral_hardness(fname)
				print '.......hard done'
				depthness = depth.timbral_depth(fname)
				print '.........depth done'

				if not brightness=='nan' or roughness=='nan' or hardness=='nan' or depthness=='nan':
					b.append(brightness)
					r.append(roughness)
					h.append(hardness)
					d.append(depthness)
					ids.append(sound_id)
					names.append(sound_name)
					class_name.append(folder)
			except:
				print '\nIgnoring feature computation of sound >>', sound
				ignore_list.append(sound)
			i = i+1
	csv_dict = {'sound_class':class_name,'sound_id':ids,'sound_name':names,'brightness':normaliseListRange(b),\
		'roughness':normaliseListRange(r),'hardness':normaliseListRange(h),'depth':normaliseListRange(d)}
	df = pd.DataFrame(csv_dict)
	df.to_csv(folder+'.csv')

	parseToJson(ids,names,b,r,h,d,folder)

	ignore = {'sounds':ignore_list}
	ig = pd.DataFrame(ignore)
	ig.to_csv('Ignore__'+folder+'.csv')

	#df.to_json(folder+'.json')
	print "\n Finished computing features for the class >>",folder

print'\nFinished computing features for all the sounds in the dataset....'


        











