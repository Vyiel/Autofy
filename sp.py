import sys
import os
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions

windows_location = str(os.environ['windir'])
rootdir = windows_location[:2]
driver_loc = rootdir+"\chromedriver"
global driver, Playlist_Found_Error
#
# try:
#     driver = webdriver.Chrome(executable_path=driver_loc)
#     driver.implicitly_wait(10)
#
# except Exception:
#     print("""Probably The chrome driver is not matched with your current Google Chrome version.
#             Please update chrome to the latest version, and download and save the latest
#             stable version of chromedriver on to the root of your Windows Installation!!! """)
#
#
# target = 'https://accounts.spotify.com/en/login?continue=https:%2F%2FoPlaylist_Found_Errorn.spotify.com%2Fbrowse%2Ffeatured'
# driver.get(target)
#
# USERNAME AND PASSWORD HERE #
# EXAMPLE :
# uname = "username"
# password = "password"

# uname = ""
# passw = ""
# playlist = ""
#
# driver.find_element_by_id("login-username").send_keys(uname)
# driver.find_element_by_id("login-password").send_keys(passw)
# driver.find_element_by_id("login-button").click()
# time.sleep(10)
# driver.find_element_by_link_text(playlist).click()
# time.sleep(5)
#
#
# body = driver.find_element_by_xpath("//ol[contains(@class, 'tracklist')]")
# element = driver.find_element_by_xpath("//div[contains(@class, 'PlaylistRecommendedTracks')]")
# actions = ActionChains(driver)
# actions.move_to_element(element)
# actions.Playlist_Found_Errorrform()
#
# time.sleep(12)
#
# label = {}
# number_of_tracks = driver.find_elements_by_xpath("//div[contains(@class, 'tracklist-col name')]")
# for items in number_of_tracks:
#     Track = items.find_element_by_xpath(".//div[contains(@class, 'tracklist-name ellipsis-one-line')]").text
#     Artist = items.find_element_by_xpath(".//span[contains(@class, 'TrackListRow__artists ellipsis-one-line')]").text
#     label[Track] = Artist
#
# file = oPlaylist_Found_Errorn("List.txt", "w", encoding='utf-8')
# for Tracks, Artists in label.items():
#     labels = Tracks + " " + Artists + "\n"
#     file.writelines(labels)
#
# time.sleep(2)
# driver.close()

# AMAZON CONVERSION #
# USERNAME AND PASSWORD HERE #
# EXAMPLE :
# uname = "username"
# password = "password"
uname = ""
passw = ""

try:
    driver = webdriver.Chrome(executable_path=driver_loc)
    driver.implicitly_wait(3)

except Exception:
    print("""Probably The chrome driver is not matched with your current Google Chrome version.
                Please update chrome to the latest version, and download and save the latest
                stable version of chromedriver on to the root of your Windows Installation!!! """)


playlist = "psychotic"
target = 'https://www.amazon.in/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=inflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&switch_account='
try:
    driver.get(target)
    print("Redirected to Amazon SignIn !!!")
except:
    print("ERROR! The redirection was not successful!!!")
time.sleep(1)

driver.execute_script('alert("Automation was not possible for 2step and OTP verification!!! Please log in within 1 minute and wait for automation to kick in!!! ");')
time.sleep(20)

target2 = "https://music.amazon.in/home"
try:
    driver.get(target2)
    driver.implicitly_wait(2)
    print("Redirected to Amazon Music!!!")
except:
    print("ERROR! Redirection was not successful!!!")
time.sleep(2)


def add_to_playlist(song):
    global driver
    time.sleep(2)
    search_box = driver.find_element_by_id('searchMusic').click()
    # print(search_box)
    time.sleep(0.5)
    driver.find_element_by_id('searchMusic').send_keys(song)
    driver.find_element_by_class_name('playerIconSearch').click()
    driver.find_element_by_class_name('playerIconSearch').click()
    time.sleep(1)
    try:
        driver.find_element_by_xpath("//div[contains(@class, 'search-navigation')]//span[text()='No results.']")
        pass
    except selenium.common.exceptions.NoSuchElementException:
        time.sleep(0.5)

        dot_options = driver.find_elements_by_xpath("//div[contains(@class, 'horizontalTile TILE')]//span[contains(@class, 'playerIconDotMenu')]")
        for icon in dot_options:
            try:
                icon.click()
                break
            except:
                continue

        menu = driver.find_element_by_xpath("//*[@id='contextMenuContainer']")
        hover = ActionChains(driver).move_to_element(menu)
        hover.perform()
        driver.find_element_by_xpath("//span[text()='Add to playlist']").click()
        time.sleep(0.5)
        driver.find_elements_by_xpath("//span[contains(@class, 'playlistTitle')]")[1].click()
        try:
            # driver.implicitly_wait(2)
            # duplicate_menu = driver.find_element_by_xpath("//div[contains(@class, 'buttonContainer')]")
            # hover = ActionChains(driver).move_to_element(duplicate_menu)
            # hover.perform()
            time.sleep(1)
            driver.find_element_by_xpath("//div[contains(@class, 'buttonContainer')]//button[text()= 'Skip']").click()
            driver.implicitly_wait(2)

        except selenium.common.exceptions.NoSuchElementException:
            pass


try:
    driver.find_element_by_xpath("//div[contains(@class, 'icon-exit closeButton')]").click()
    print("Language Preference Popped up, and closed")
except selenium.common.exceptions.NoSuchElementException as e:
    print("Language Preference Popup didn't exist")

try:
    driver.find_element_by_link_text(playlist)
    print("playlist found, Will skip to adding tracks")
    Playlist_Found_Error = False
except selenium.common.exceptions.NoSuchElementException as e:
    # print(e)
    print("Playlist not Found, Will be created")
    Playlist_Found_Error = True
    driver.find_element_by_id("newPlaylist").click()
    time.sleep(.5)
    driver.find_element_by_id("newPlaylistName").send_keys(playlist)
    time.sleep(.5)
    driver.find_element_by_class_name("buttonOption").click()
    time.sleep(3)

songs = ["Something's Gotta Give Camila Cabello", "asdafava", "Daydream Medasin, Joba", "Daydream Medasin, Joba"]

if Playlist_Found_Error is False:
    time.sleep(2)
    for i in songs:
        add_to_playlist(i)
    # add_to_playlist("Something's Gotta Give Camila Cabello")


# # driver.find_element_by_id('searchMusic').send_keys(song).send_keys(Keys.RETURN)






