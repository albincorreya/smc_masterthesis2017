#==========================================
'''
Python script to extract timbral features from audiocommons timbral models
from the specified dataset and store it as a JSON file for every sound classes.


This script uses timbral models developed by Andy Pearce as a part of AuioCommons intiative.
You can find it here -> https://github.com/AudioCommons/timbral_models.



Use : pass the full directory path of you dataset to the script as command-line argument in the terminal.
	python multiclass_timbralfeature_extractor.py <your_path>

-------
Albin Andrew Correya
Music Technology Group
UPF
'''
#==========================================


import sys
import pandas as pd
import os, json, csv

from progressbar import ProgressBar
pbar = ProgressBar()


# clone or download the timbral model from https://github.com/AudioCommons/timbral_models
import Timbral_Brightness as bright
import Timbral_Roughness as rough
import Timbral_Depth as depth
import Timbral_Hardness as hard




def normaliseListRange(myList):
	'''
	Function to normalise the elements in a list to the range (0,100)
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
#path = '/Users/Correya/desktop/Master_Thesis/freesound_dataset/client_download_freesound/100_fs_dataset/'

def main(path,normalise=False):
	folders = os.listdir(path)
	if '.DS_Store' in folders:    #remove the hidden file in the folders in mac osx
		folders.remove('.DS_Store')

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

		# Parse and save the lists into the required json format (without normalising the values)
		if normalise is True:
			parseToJson(ids,names,normaliseListRange(b),normaliseListRange(r),normaliseListRange(h),normaliseListRange(d),folder)
		if normalise is False:
			parseToJson(ids,names,b,r,h,d,folder) 

		# Parse and save it to a csv file (with normalising the values to the range 0-100)
		csv_dict = {'sound_class':class_name,'sound_id':ids,'sound_name':names,'brightness':normaliseListRange(b),\
			'roughness':normaliseListRange(r),'hardness':normaliseListRange(h),'depth':normaliseListRange(d)}
		df = pd.DataFrame(csv_dict)
		df.to_csv(folder+'.csv')

		# Save the list of ignored sounds during the extraction process and save it as csv file
		ignore = {'sounds':ignore_list}
		ig = pd.DataFrame(ignore)
		ig.to_csv('Ignore__'+folder+'.csv')

		print "\n Finished computing features for the class >>",folder

	print'\nFinished computing features for all the sounds in the dataset....'



if __name__ == '__main__':
	try:
		path = sys.argv[1]
		main(path)
	except:
		print('Please pass the full directory path.....')





