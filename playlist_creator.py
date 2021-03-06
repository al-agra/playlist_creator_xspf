import os
import random


def Rand(start, end, num): 
	#This function will generate a list of random integers, choosing between start and end, for a count of num, and return a list.
    res = [] 
  
    for j in range(num): 
        res.append(random.randint(start, end)) 
  
    return res 


def get_filepaths(directory):
    
    #This function will generate the file names in a directory 
    #tree by walking the tree either top-down or bottom-up. For each 
    #directory in the tree rooted at directory top (including top itself), 
    #it yields a 3-tuple (dirpath, dirnames, filenames).
   
	file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root,directories,files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable.   

#Main Program

music_file_paths = get_filepaths(r"C:\Users\User\Desktop\Test\Music") #Choose your own music folder path
spots_file_paths = get_filepaths(r"C:\Users\Alex\Desktop\Test\Spots") #Choose your own ad spot folder path
print(music_file_paths)
print(spots_file_paths)

#If .xspf file already exists, delete it.
path = r"C:\Users\User\Desktop" #Choose where you want your playlist file to be crated
for filename in os.listdir(path):
    if(filename == "list.xspf"):
        os.remove("list.xspf")
	
#Create a .txt file with name list. If it already exists, delete previous and create a new one.

try:
  playlist = open("list.txt", "x")
except: 
    os.remove("list.txt")
    playlist = open("list.txt", "x")

#This is where the playlist is created.
#First, we write the header required for the xspf file format.

playlist.write("""<?xml version="1.0" encoding="UTF-8"?>
<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">
	<title>Paprika</title>
	<trackList>\n""") 


random_list = Rand(0,len(music_file_paths)-1,len(music_file_paths)-1)
song_index = 0 
ad_count = 0   #Ad index, caps at len(spots_file_path)
song_count = 0 
for song in music_file_paths: 
    song_index = random_list[song_count-1]
    playlist.write("<track><location>"+ music_file_paths[song_index]+ "</location></track>\n")
    song_count = song_count + 1
    if((song_count) % 3 == 0): #Change the number 3 to how many music tracks you want between ads.
        if((ad_count + 1) % len(spots_file_paths) == 0):
            playlist.write("<track><location>"+spots_file_paths[ad_count]+"</location></track>\n")
            ad_count = 0
        else: 
            playlist.write("<track><location>"+spots_file_paths[ad_count]+"</location></track>\n")
            ad_count += 1

#Finally, we end the playlist
playlist.write("""</trackList>
	<extension application="http://www.videolan.org/vlc/playlist/0">
	</extension>
</playlist>""") 

#close the file
playlist.close()

#Convert .txt to .xspf 
for filename in os.listdir(path):
    if(filename == "paprika_list.txt"):
        filename_without_ext = os.path.splitext(filename)[0]
        extension = ".xspf"
        new_file_name = filename_without_ext 
        new_file_name_with_ext = new_file_name+extension
        print(new_file_name_with_ext)
        os.rename(os.path.join(path,filename),os.path.join(path,new_file_name_with_ext))
