
import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
import pymongo







class Kitap_Sepeti():
    " That class enters the Kitap Sepeti website and taking book name, book publisher, book writer and book price"
    

    def Mine_Url(self,i):
        "That fonk. giving url adress"

        mainurl = "https://www.kitapsepeti.com"
        url_list = ["/roman","/egitim","/felsefe","/cocuk-kitaplari","/gezi-ve-rehber-kitaplari","/saglik","/insan-ve-toplum","/inanc-kitaplari-mitolojiler"
                    ,"/psikoloji","/hukuk","/islam"]
        return mainurl + url_list[i] 

    def Go_to_url(self,browser,url):
        "That fonk. only going to url"
        return browser.get(url)

    def Browser(self):
        "That fonk. only returning browser driver not taking any object"

        return webdriver.Chrome()


    def MineData(self,url):
        "That fonk. going to website and mine all data"

        getc = requests.get(url) # determining the site
        contentc=getc.content # pulling the site source and assigning it to a variable
        #print(rr)

        soup = BeautifulSoup(contentc,"html.parser") # I get all html codes from this source
        html = soup.find_all("div",{"class":"col col-3 col-md-4 col-sm-6 col-xs-6 p-right mb productItem zoom ease"}) #simplifying html codes 
        
        list = [] # I'm throwing an empty list
        
        for code in html: # I edit the simplified source by navigating through the site code
        #code.get("href")
            test = str(code.text) # I get the page source as text and str for the editing process

            if test[0] != "<": # simplifying the source
                a=test.split("\n") # simplifying again for the gaps

                for i in a: # I only get the book title, publishing house name, author and book price.

                    if (len(i)>3 and i !="Sepete Ekle" ): # again simplifying the source
                        list.append(i)
                        #print(i)

        groups = [list[i:i+4] for i in range(0,len(list),4)]
        return groups
    
    def Mining(self):
        "That fonk. going to website and mine all data"

        browser = self.Browser()
        for i in range(11): #To navigate pages to book genres

            url = self.Mine_Url(i)
            self.Go_to_url(browser=browser,url=url)
            time.sleep(2)
            browser.find_element(By.XPATH,"//*[@id='filtreStock']/div/div/div/div/label").click() #marking what is in stock
            time.sleep(1)
            total_pagenum=browser.find_element(By.XPATH,"//*[@id='pager-wrapper-top']/div/div/a[10]").text #taking last page
            time.sleep(2)

            for i in range(1,int(total_pagenum)):

                now_url = browser.current_url # retrieving used url
                type = url.split("/")[-1] # taking book type 
                data = self.MineData(now_url) # thml data mining
                for j in data:
                    
                    self.Data_Save(type=type, pagenumber=i , book_names=j[0], book_publishers=j[1], book_writers=j[2], book_price=j[3] ) #data saving
                    time.sleep(1)

                browser.find_element(By.XPATH,"//*[@id='pager-wrapper-top']/div/div/a[11]").click() # next
                time.sleep(2)

    def Data_Save(self,type,pagenumber,book_names,book_publishers, book_writers, book_price):
        "That fonk. saving data in MongoDB data base"

        book_price = book_price +" ₺" #adding turk liras symbol
        myclient = pymongo.MongoClient("mongodb://localhost:27017/") #server settings
        mydb = myclient["smartmaple"] # for informatiıon
        mycol = mydb["kitapsepeti"] # for information
        
        book_data = {"Type": type, "Page Number": pagenumber, "title": book_names, "publisher": book_publishers, "writers": book_writers, "Book Price": book_price} # writing data
        return mycol.insert_one(book_data) 


        


        

Kitap_Sepeti().Mining()