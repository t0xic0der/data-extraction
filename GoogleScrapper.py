import requests, time, os
from selenium import webdriver

def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    wd.get(search_url.format(q=query))
    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < int(max_links_to_fetch):
        scroll_to_end(wd)
        thumbnail_results = wd.find_elements_by_css_selector("img.rg_ic")
        number_results = len(thumbnail_results)
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        for img in thumbnail_results[results_start:number_results]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue
            actual_images = wd.find_elements_by_css_selector('img.irc_mi')
            for actual_image in actual_images:
                if actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))
            image_count = len(image_urls)
            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(1)
            load_more_button = wd.find_element_by_css_selector(".ksb")
            if load_more_button:
                wd.execute_script("document.querySelector('.ksb').click();")
        results_start = len(thumbnail_results)
    return image_urls

def main():
    print("IMAGE SCRAPPER by t0xic0der")
    name=input("What images do you wish to gather? ")
    cont=input("How many images do you wish to gather? ")
    loca=input("What is your webdriver's location? ")
    #loca="/home/t0xic0der/Scrapping/chromedriver"
    wbdv=webdriver.Chrome(executable_path=loca)
    imlc=fetch_image_urls(name,int(cont),wbdv,1)
    for indx in imlc:
        print("Downloading from "+str(indx)+"... ")
        os.system("wget "+str(indx))

main()
