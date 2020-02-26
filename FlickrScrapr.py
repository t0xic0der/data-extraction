# t0xic0der

import requests, os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# How long the script should wait for the page elements to load correctly
# Default is 1 second (DO NOT MODIFY IF YOU DO NOT KNOW WHAT IT IS)
sliptime=1

# How long should the script wait before timing out on thumbnail fetch?
# Set HIGHER value on slower connections and LOWER value of faster ones
# Default is 5 seconds (if sliptime is set to 1)
tumbtime=5

# How long should the script wait before timing out on download fetch?
# Set HIGHER value on slower connections and LOWER value of faster ones
# Default is 5 seconds (if sliptime is set to 1)
icontime=5

def getimage(qury:str, mxft:int, brws:webdriver):
    urgt="https://www.flickr.com/search/?text="+qury
    brws.get(urgt)
    imageset=[]
    try:
        for i in range(0,mxft):
            tumbcont,iconcont=0,0
            print("Found some results! Picking "+str(i)+"th image from them")
            tumbflag=False
            while tumbflag is False:
                try:
                    picktumb=brws.find_elements_by_class_name("overlay")
                    picktumb[i].click()
                    print("Image thumbnail found! Lets go")
                    iconflag=False
                    while iconflag is False:
                        try:
                            actlimag=brws.find_element_by_css_selector("i.ui-icon-download")
                            print("Download icon found! Lets go")
                            actlimag.click()
                            viewsize=brws.find_element_by_css_selector("a.all-sizes")
                            viewsize.click()
                            subedown=brws.find_element_by_id("allsizes-photo")
                            download=subedown.find_element_by_tag_name("img")
                            imageset.append(download.get_attribute("src"))
                            brws.back()
                            brws.back()
                            brws.refresh()
                            iconflag=True
                        except:
                            iconcont+=1
                            print("Download icon not found! Waiting for ONE second ["+str(iconcont)+"/"+str(icontime)+"]")
                            if (iconcont>=icontime):
                                print("Timeout occurred while fetching download icon. Displaying incomplete results.")
                                print(imageset)
                                exit()
                            else:
                                time.sleep(sliptime)
                    tumbflag=True
                except:
                    tumbcont+=1
                    print("Image thumbnail not found! Waiting for ONE second ["+str(tumbcont)+"/"+str(tumbtime)+"]")
                    if (tumbcont>=tumbtime):
                        print("Timeout occurred while fetching thumbnails. Displaying incomplete results.")
                        print(imageset)
                        exit()
                    else:
                        time.sleep(sliptime)
    except KeyboardInterrupt:
        print(imageset)
    print("\nFetch SUCCEEDED! Here are the results")
    print(imageset)
    savefile(imageset)

def savefile(imageset):
    for link in imageset:
        print("\nDownloading "+link+"...")
        os.system("wget "+link)
    print("Successfully downloaded "+str(len(imageset))+" images!")

def main():
    print("FLICKR SCRAPR by t0xic0der")
    qury=input("Enter the query that you wish to search ")
    mxft=input("Enter the number of images you are looking for ")    
    loca=input("Enter the location of the web driver ")
    brws=webdriver.Chrome(executable_path=loca)
    getimage(qury,int(mxft),brws)

main()
    
