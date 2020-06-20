from flask import Flask,render_template,request,redirect,url_for
from selenium import webdriver
from time import sleep
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


app = Flask(__name__)
@app.route("/")
def index():
    numbers =[1,2,3,4,5]
    return render_template("index.html",number=10,message="deneme mesajı",numbers= numbers)

@app.route("/deneme",methods = ["GET","POST"])
def deneme():
    if request.method == "POST":
        inputSite = request.form.get("inp")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get("https://www.google.com/")
        driver.find_element_by_xpath("/html/body/div/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input").send_keys(inputSite)
        driver.find_element_by_name("btnK").click()
        driver.find_element_by_xpath("/html/body/div[6]/div[2]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/a/h3").click()
        return render_template("deneme.html",source=driver.page_source,inputSite=request.form.get("inp"))
    else:
        
        return render_template("deneme.html")

@app.route("/unfollowers",methods = ["GET","POST"])
def unfollowers():
    if request.method == "POST":
        userName = request.form.get("username")     
         
        unfollowers = []

        class InstaBot:

            def __init__(self, username, pw):
                self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
                self.driver.get("https://www.instagram.com/")
                sleep(2)
                self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
                   .send_keys(username)
                self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
                   .send_keys(pw)
                self.driver.find_element_by_xpath('//button[@type="submit"]')\
                   .click()
                sleep(2)
                
                

            #finding names of unfollowers
            def get_unfollowers(self):
                self.driver.get("https://www.instagram.com/" + userName)
                sleep(2)
                try:
                    self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()                  
                except Exception:
                    self.driver.find_element_by_xpath("//button[text()='Takip Et']").click()
                #wait =  WebDriverWait(self.driver,30)
                #takipEdildi = wait.until(ec.visibility_of_element_located((By.XPATH, "//a[contains(@href,'/following')]")))
                    sleep(10)
                    self.driver.refresh()
                    self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()    
                        
                following = self._get_names()
                self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
                  .click()
                followers = self._get_names_followers()

                for user in following:
                    if user not in followers:
                        unfollowers.append(user)
                
                    
            
            #finding names of following
            def _get_names(self):
                sleep(2)
                #sugs = self.driver.find_element_by_xpath('/html/body/div[4]/div/nav/a[1]')
                #self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
                sleep(2)
                scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
                last_ht, ht = 0, 1
                while last_ht != ht:
                    last_ht = ht
                    sleep(1)
                    ht = self.driver.execute_script("""
                        arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                        return arguments[0].scrollHeight;
                        """, scroll_box)
                links = scroll_box.find_elements_by_tag_name('a')
                names = [name.text for name in links if name.text != '']
                # close button
                sleep(1)
                self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button")\
                   .click()
                return names

            #finding names of followers
            def _get_names_followers(self):
                sleep(2)
                scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
                last_ht, ht = 0, 1
                while last_ht != ht:
                   last_ht = ht
                   sleep(1)
                   ht = self.driver.execute_script("""
                      arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                      return arguments[0].scrollHeight;
                      """, scroll_box)
                links = scroll_box.find_elements_by_tag_name('a')
                names = [name.text for name in links if name.text != '']
                # close button
                sleep(1)
                self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button")\
                   .click()
                return names

        my_bot = InstaBot('towig92092','zaxscdvfbg')
        my_bot.get_unfollowers()   

        return render_template("/unfollowers.html",unfollowers = unfollowers)
    else:
        return redirect(url_for("index")) 

if __name__ == "__main__":
    app.run(debug = True)