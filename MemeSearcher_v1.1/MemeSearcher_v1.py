import requests
import os
import re

headers = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
results = []
results_cleaned = []
results_processed = []
results_showing = []
ranking_selected = 10
url = 'https://www.fabiaoqing.com/search'


response = requests.get(url,headers = headers)
text = response.text 
results = re.findall('<a\shref="(.*?)"',text) 
###print("rawdata",results)


count = 1
for result in results:
    result_cleaned = re.sub('100.*?com','',result)
    results_cleaned.append(result_cleaned)
    result_showing = re.sub('http://fabiaoqing.com/search/search/keyword/','',result_cleaned)
    result_showing = str(count) + result_showing
    results_showing.append(result_showing)
    ###print("showingdata",result_showing)
    print(result_showing)
    count += 1
print("The updated ranking are showing above")
###print(count)


while True:
    temp_num = input("Please enter a integer indicating the downloading range, the default value is top 10: ")
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
    ranking_selected = int(temp_num)
###print(results_cleaned)


#print("ranking",ranking_selected)
results_cleaned = results_cleaned[0:int(ranking_selected)]
###print("results_cleaned", results_cleaned)
for result_cleaned in results_cleaned:
    result_processed = re.sub('\s','%20',result_cleaned)
    results_processed.append(result_processed)  
print("processedData",results_processed)


dirCount = 0
for url in results_processed:
        response = requests.get(url,headers = headers) 
        text = response.text 
        picResults = re.findall('data-original="(.*?)"\stitle="(.*?)"',text)
        print("eachPic",picResults) #[picUrl][picName]     
        
        fullPath = os.path.join(os.path.expanduser('~'),"Desktop","Meme",results_showing[dirCount])
        if not os.path.exists(fullPath): 
            os.makedirs(fullPath)
        try:
            for picResult in picResults:
                image = requests.get(picResult[0])  
                path = os.path.join(fullPath,picResult[1]) 
                print("saving",path)
                with open(path+".gif",mode = "wb") as f:
                    f.write(image.content)            
        except Exception as err:
            print("Error skipped:",err)
            pass
        dirCount += 1
   