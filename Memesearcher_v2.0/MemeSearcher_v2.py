#Memesearcher_v2
#Kyekyekye
#1/14/2010

import requests
import os
import re


headers = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
url = 'https://www.fabiaoqing.com/search'    

def get_page():
    response = requests.get(url,headers = headers)
    text = response.text 
    results = re.findall('<a\shref="(.*?)"',text)
    ###print("rawdata",results)
    return results
    
def data_cleaning(results):
    results_cleaned = []
    for result in results:
        result_cleaned = re.sub('100.*?com','',result)
        results_cleaned.append(result_cleaned)
        
    ###print(results_cleaned)
    return results_cleaned
              
def ranking_showing(results_cleaned):        
    count = 1
    results_showing = []
    for result_cleaned in results_cleaned:
        result_showing = re.sub('http://fabiaoqing.com/search/search/keyword/','',result_cleaned)
        result_showing = str(count) + result_showing
        results_showing.append(result_showing)
        ###print("showingdata",result_showing)
        print(result_showing)
        count += 1
    print("The updated ranking are showing above")
    return results_showing
    ###print(count)
   
def ask_option():
    print("------------------------------------------------------------------")
    print("1 Overall Searching\n2 Deep Searching\nPlease choose you option: ")
    while True:
        temp_num = input()    
        if temp_num == '1':
            break
        elif temp_num == '2':
            break
        else:
            print("Invaild input.") 
    return temp_num
 
def ask_depth(count):
    print("------------------------------------------------------------------")
    while True:
        temp_num = input("Please enter the ranking of the keyword you want to deep searching  ")
        if temp_num.isdigit():
            if int(temp_num) < count:
                break
            else:    
                print("Invaild input.")
        elif temp_num == "":
            break
        else:
            print("Invaild input.")  
    return temp_num

def make_deepUrl(results_cleaned,ranking):
    result_cleaned = results_cleaned[int(ranking)-1]
    result_processed = re.sub('\s','%20',result_cleaned)
    return result_processed
 
def ask_range(count):
    print("------------------------------------------------------------------")
    while True:
        temp_num = input("Please enter downloading range, the default value is top 10: ")
        if temp_num.isdigit():
            if int(temp_num) < count:
                break
            else:    
                print("Invaild input.")
        elif temp_num == "":
            break
        else:
            print("Invaild input.")     
    if temp_num != "":
        return int(temp_num)
    else:
        return 10
    ###print(results_cleaned)
    ###print("ranking",ranking_selected)
  
def make_url(results_cleaned,ranking):
    results_cleaned = results_cleaned[0:int(ranking)]
    ###print("results_cleaned", results_cleaned)
    results_processed = []
    for result_cleaned in results_cleaned:
        result_processed = re.sub('\s','%20',result_cleaned)
        results_processed.append(result_processed)     
    ###print("processedData",results_processed)
    return results_processed

def pic_deepDownload(result_processed,foldName):
    picCount = 1
    pageCount = 1
    
    fullPath = os.path.join(os.path.expanduser('~'),"Desktop","Meme",foldName)
    if not os.path.exists(fullPath): 
        os.makedirs(fullPath)
    
    while True:
        url = result_processed + "/type/bq/page/" + str(pageCount) + ".html"
        ###print("url", url)
        pageCount += 1
        response = requests.get(url,headers = headers) 
        text = response.text 
        picResults = re.findall('data-original="(.*?)"\stitle="(.*?)"',text) 
        
        try:
            for picResult in picResults:
                suffix = re.search('http.*(\..*)$',picResult[0])
                image = requests.get(picResult[0])  
                path = os.path.join(fullPath,picResult[1]) 
                print("saving",path)
                picCount += 1
                with open(path+ suffix.group(1) ,mode = "wb") as f:
                    f.write(image.content)            
        except Exception as err:
            print("Error skipped:",err)
            pass

        temp = input(str(picCount) + "memes downloaded/updated, \npress 'x' to finish,\nor press Enter to continue...")
        if temp == 'x':
            break

def pic_download(results_processed,results_showing):
    dirCount = 0
    for url in results_processed:
            response = requests.get(url,headers = headers) 
            text = response.text 
            picResults = re.findall('data-original="(.*?)"\stitle="(.*?)"',text)
            fullPath = os.path.join(os.path.expanduser('~'),"Desktop","Meme",results_showing[dirCount])
            if not os.path.exists(fullPath): 
                os.makedirs(fullPath)
            try:
                for picResult in picResults:
                    suffix = re.search('http.*(\..*)$',picResult[0])
                    image = requests.get(picResult[0])  
                    path = os.path.join(fullPath,picResult[1]) 
                    print("saving",path)
                    with open(path+ suffix.group(1) ,mode = "wb") as f:
                        f.write(image.content)            
            except Exception as err:
                print("Error skipped:",err)
                pass
            dirCount += 1
    print("downloading/updating finished")
                      
def main():
    results = get_page()
    results_cleaned = data_cleaning(results)
    results_showing = ranking_showing(results_cleaned)
    results_range = len(results_cleaned)
    
    while True:
        option = ask_option()
        if option == '1':
            ranking = ask_range(results_range)
            results_processed = make_url(results_cleaned,ranking)
            pic_download(results_processed,results_showing)
        if option == '2':
            ranking = ask_depth(results_range)
            result_processed = make_deepUrl(results_cleaned,ranking)
            foldName = results_showing[int(ranking)-1]
            pic_deepDownload(result_processed,foldName)

main()