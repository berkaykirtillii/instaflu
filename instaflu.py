from flask import Flask,render_template,request,redirect,url_for
from selenium import webdriver
from time import sleep

app = Flask(__name__)
@app.route("/")
def index():
    numbers =[1,2,3,4,5]
    return render_template("index.html",number=10,message="deneme mesajı",numbers= numbers)

@app.route("/deneme")
def deneme():
    return render_template("deneme.html")

@app.route("/unfollowers",methods = ["GET","POST"])
def learnUnfollowers():
    if request.method == "POST":
        userName = request.form.get("username")     
         
        list_unfollowers = []

        class InstaBot:

            def __init__(self, username, pw):
                self.driver = webdriver.Chrome("chromedriver\chromedriver.exe")
                self.driver.get("https://www.instagram.com/")
                sleep(2)
                self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
                   .send_keys(username)
                self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
                   .send_keys(pw)
                self.driver.find_element_by_xpath('//button[@type="submit"]')\
                   .click()
                sleep(4)
                self.driver.find_element_by_xpath("//button[contains(text(), 'Şimdi Değil')]")\
                   .click()
                if(self.driver.find_element_by_xpath("//button[contains(text(), 'Şimdi Değil')]")):
                    self.driver.find_element_by_xpath("//button[contains(text(), 'Şimdi Değil')]")\
                        .click()
                sleep(2)

            #finding names of unfollowers
            def get_unfollowers(self):
                self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")\
                  .send_keys(userName)
                sleep(2)
                self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]")\
                  .click()
                sleep(2)
                self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
                  .click()
                following = self._get_names()
                self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
                  .click()
                followers = self._get_names_followers()

                for user in following:
                    if user not in followers:
                        list_unfollowers.append(user)
                
                    
            
            #finding names of following
            def _get_names(self):
                sleep(2)
                sugs = self.driver.find_element_by_xpath('/html/body/div[4]/div/nav/a[1]')
                self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
                sleep(2)
                scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
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
                self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
                   .click()
                return names

            #finding names of followers
            def _get_names_followers(self):
                sleep(2)
                scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
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
                self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
                   .click()
                return names

        my_bot = InstaBot('towig92092','zaxscdvfbg')
        my_bot.get_unfollowers()   

        return render_template("/unfollowers.html",list_unfollowers = list_unfollowers)
    else:
        return redirect(url_for("index")) 


if __name__ == "__main__":
    app.run(debug = True)