
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

        r = requests.get(url) # site belirleniyor
        rr=r.content # site kaynağı çekilerek bir değişkene atıyorum
        #print(rr)
        soup = BeautifulSoup(rr,"html.parser") # bu kaynaktaki tüm html kodlarını alıyorum
        a = soup.find_all("div",{"class":"col col-3 col-md-4 col-sm-6 col-xs-6 p-right mb productItem zoom ease"}) #html kodlarını sadeleştiriyorum 
        list = [] # boş bir liste atıyorum
        for ass in a: # site kodları içinde gezinerek sadeleşmiş kaynağı düzenliyorum
        #ass.get("href")
            test = str(ass.text) # düzenleme işlemi için sayfa kaynağını text ve str olarak alıyorum
            if test[0] != "<": # kaynak sadeleştiriyorum
                a=test.split("\n") # boşluklar için yine sadeleştiriyorum
                for i in a: # sadece kitap ismi , yayın evi ismi, yazar ve kitap fiyatını alıyorum.
                    if (len(i)>3 and i !="Sepete Ekle" ): # yine sadeleştiriyorum. 
                        list.append(i)
                        #print(i)

        gruplar = [list[i:i+4] for i in range(0,len(list),4)]
        return gruplar
    
    def Mining(self):
        "That fonk. going to website and mine all data"

        browser = self.Browser()
        for i in range(11): #Kitap türlerine giden sayfaları gezmek için

            url = self.Mine_Url(i)
            self.Go_to_url(browser=browser,url=url)
            time.sleep(2)
            browser.find_element(By.XPATH,"//*[@id='filtreStock']/div/div/div/div/label").click() #stokta olanları işaretliyor
            time.sleep(1)
            total_pagenum=browser.find_element(By.XPATH,"//*[@id='pager-wrapper-top']/div/div/a[10]").text #son sayfayı alıyor.
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