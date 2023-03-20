import os
import csv
import re
from glob import glob
import requests

#Welcome on Discord data package extractor.
#--- Proudly made by Ech0 ---")
print("----------------------------------------------")
print("Welcome to Discord DATAPACKAGE Extractor V1.0")
print("----------------------------------------------")
PATH_FOR_IMAGE_EXTRACTION = input("Please enter the path for the image extraction (PLEASE BE CAREFULL where you download the files): ")
PATH = input("Please enter the path to your data package: ")
# DO NOT MODIFY ANY PARAMETER IN THE CODE
if (PATH_FOR_IMAGE_EXTRACTION[len(PATH_FOR_IMAGE_EXTRACTION)-1] != "/"):
    PATH_FOR_IMAGE_EXTRACTION = PATH_FOR_IMAGE_EXTRACTION + "/"
    print("Path for extraction ok. (Added / at the end of the path)")
else :
    print("Path for extraction ok.")
if (PATH[len(PATH)-1] != "/"):
    PATH = PATH + "/"
    print("Path to data package ok. (Added / at the end of the path)")
#----------
print("----------------------------------------------")
print("Here is the path for the package : "+PATH)
print("Here is the path to the destination folder : "+PATH_FOR_IMAGE_EXTRACTION)
print("----------------------------------------------")
before_start_breaker = 0
while (before_start_breaker == 0):
    before_start = input("Extraction and download of all images is going to begin. Continue ? y / n :")
    if (before_start == "n"):
        print("Interrupted. Bye.")
        exit()
    if (before_start == "y"):
        before_start_breaker = 1
        print("Processing. . .")
#-- 1 -- EXTRACTING INTERESTING ELEMENTS FROM THE DATAPACKAGE
all_img_link = [] #All the links and other similar expression
final_links = [] #Will be used to store the images link list
EXT = "*.csv" #Select all CSV files in folder and subfolders.
all_csv_files = [file
                 for path, subdir, files in os.walk(PATH)
                 for file in glob(os.path.join(path, EXT))]


#-- 2 -- FILTERING FOR ALL IMAGES BELONGING TO DISCORD CDN
for csv_to_open in range(0, len(all_csv_files)): #Filtering all images on DiscordCDN
    csv_trt = all_csv_files[csv_to_open]
    cr = csv.reader(open(csv_trt))
    for row in cr:
        current_row = str(row)
        if("https://cdn.discordapp.com" in current_row):
            all_img_link.append(current_row)

#-- 3 -- DOING SOME TREATMENTS ON THE LIST TO MAKE IT USABLE
for row_links in range(0, len(all_img_link)): #Preparing the link : Removing any square braces, commas etc.
    current_row_links = all_img_link[row_links]
    for char in range(0, len(current_row_links)):
        if current_row_links[char] == "h":
            index_first_url_char = char
            break;
    for char in range(0, len(current_row_links)):
        if current_row_links[char] == "'":
            index_last_url_char = char
    final_url = current_row_links[index_first_url_char:index_last_url_char]
    trt = final_url.split()
    for y in range(0, len(trt)) :
        if trt[y] == "'":
            index_last_url_char = y
    final_url_ready = final_url[0:index_last_url_char]
    final_links.append(final_url_ready)

#-- 4 -- PREPARING ALL THE URLS, CHECKING FOR DUPP AND FILTERING EVERYTHING THAT IS NOT A URL.
buffer_links_cleared = [] #Checking if all the elements in the list are urls, it may arrive that some characters appears as url.
for all_links in range(0, len(final_links)):
    buffer_links = final_links[all_links]
    if (buffer_links.startswith('https') == True and len(buffer_links) > 20): #All discord links len are > to 20 char. We also check it start with https
        buffer_links_cleared.append(buffer_links)
final_links = buffer_links_cleared

final_links = list(dict.fromkeys(final_links)) #Deleting dupplicated in the final list.

#print(final_links) #USED TO DEBUG AND SEE ALL THE LINKS
print("----------------------------------------------")
print("NUMBERS OF ELEMENTS TO DOWNLOAD", len(final_links))
print("----------------------------------------------")
#-- 5 -- DOWLOADING ALL THE IMAGES
i = 0 #Used to generates the image name and the download tracking
for elements in range(0, len(final_links)) :
    print("Downloading image : "+str(i)+" on "+str(len(final_links)))
    file_name = PATH_FOR_IMAGE_EXTRACTION+str(i)+".png"
    try:
        with open(file_name, 'wb') as f:
            f.write(requests.get(final_links[elements]).content)
    except ValueError:
        print("Image with index N* "+str(i)+" could not be extracted ;-(")
    i = i+1
