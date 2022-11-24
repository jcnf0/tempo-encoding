import madmom
from pydub import AudioSegment
from subprocess import call
from madmom.features.beats import RNNBeatProcessor
from madmom.features.tempo import TempoEstimationProcessor
proc=TempoEstimationProcessor(fps=100)

#Folder where the operations will be made
export_folder="/mnt/d/UbuntuFolder/Playtest/"

#Tempi analysis of the song with madmom
def tempi(song):
	act=RNNBeatProcessor()(song)
	return proc(act)

#Slightly modifies the tempo to encode a 1
def bit0(segment,rate):
	print("Modifying tempo of segment by -"+"{:02d}".format(rate))
	call(["soundstretch", segment, segment, "-tempo=-{:.1f}".format(rate)])
	print("Done")
	return None

#Slightly modifies the tempo to encode a 0
def bit1(segment,rate):
	print("Modifying tempo of segment by +"+"{:02d}".format(rate))
	call(["soundstretch", segment, segment, "-tempo={:.1f}".format(rate)])
	print("Done")
	return None

#Function used to preprocess the music and split it in constant tempo segments
def cut(song,phi,rate,name):
	print("Loading tempo from librosa...")
	y,sr=librosa.load(song)
	duration=librosa.get_duration(y,sr=sr)
	onset_env=librosa.onset.onset_strength(y,sr=sr)
	dtempo=librosa.beat.tempo(onset_envelope=onset_env,sr=sr)
	print("Done.")
	Segments=[]
	Seg=[]
	Seg.append(0)
	print("Segment separation...")
	for i in range(len(dtempo)-1):
		if abs(tempo[i]-tempo[i+1])<=tempo[i]/200:
			Seg.append(i+1)
		else:
			Segments.append(L)
			Seg=[]
			Seg.append(i+1)
	print("Done.")
	print("Generating segments...")
	DurSeg=[duration/len(Segments[k]) for k in range(len(Segments))]
	t=0
	for i in range(len(Segments)):
		t1=t*1000
		t2=(DurSeg[i]+t)*1000
		t+=DurSeg[i]
		newAudio=AudioSegment.from_wav(song)
		newAudio=newAudio[t1:t2]
		newAudio.export("{}{}segment{:02d}.wav".format(export_folder,name,i),format="wav")
	print("Done.")
	return len(Segment)

#Encode a segment by splitting it in sub-segments of length phi
def encode_segment(segment,msg,phi,rate,tag):
	duration=librosa.get_duration(filename=segment)
	nb_bits=floor(duration/(phi*1.1))
	if nb_bits<2:
		return 0
	SSegsPath=[]
	for k in range(nb_bits):
		t1=k*phi*1000
		t2=(k+1)*phi*1000
		newAudio=AudioSegment.from_wav(segment)
		newAudio=newAudio[t1:t2]
		newAudio.export("{}sseg{}{:02}.wav".format(export_folder,tag,k),format="wav")
		SSegsPath.append("{}sseg{}{:02}.wav".format(export_folder,tag,k))
	Merger=0
	for k in range(nb_bits):
		if int(msg[k])==0:
			bit0(SSegsPath[k],rate)
		elif int(msg[k])==1:
			bit1(SSegsPath[k],rate)
		Merger+=AudioSegment.from_wav(SSegsPath[k])
		#call(["rm",SSegsPath[k]])
	Merger.export(segment,format="wav")
	return nb_bits

#Encode the whole song by using the previous functions
def encode(song,msg,phi,rate,tag,name):
	code=msg
	nb_seg=cut(song,phi,rate,name)
	for k in range(nb_seg):
		segment="{}segment{:02d}.wav".format(export_folder,k)
		sub_tag=tag+'{}'.format(k)
		decalage=encode_segment(segment,code,phi,rate,sub_tag)
		code=code[decalage::]
	Merger=0
	for k in range(nb_seg):
		Merger+=AudioSegment.from_wav("{}{}segment{:02d}.wav".format(export_folder,name,i))
	Merger.export("{}{}modified.wav".format(export_folder,name),format="wav")
	return None

if __name__=='__main__':
	print('Song to encode :')
	song=input()

	print('Message to encode (0/1) :')
	msg=input()

	print('Phi (s):')
	phi=input()

	print('Rate (%):')
	rate=input()

	print('Tag :')
	tag=input()

	print('Name :')
	name=input()

	encode(song,msg,phi,rate,tag,name)
	
	
