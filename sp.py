import sys
import os
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

windows_location = str(os.environ['windir'])
rootdir = windows_location[:2]
driver_loc = rootdir+"\chromedriver"
global driver, Playlist_Found, Playlist_Created, wait

def spotify_render_list():
    try:
        driver = webdriver.Chrome(executable_path=driver_loc)
        driver.implicitly_wait(10)

    except Exception:
        print("""Probably The chrome driver is not matched with your current Google Chrome version.
                Please update chrome to the latest version, and download and save the latest
                stable version of chromedriver on to the root of your Windows Installation!!! """)


    target = 'https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2Fbrowse%2Ffeatured'
    driver.get(target)

    # USERNAME AND PASSWORD HERE #
    # EXAMPLE :
    # uname = "username"
    # password = "password"

    uname = ""
    passw = ""
    playlist = ""

    driver.find_element_by_id("login-username").send_keys(uname)
    driver.find_element_by_id("login-password").send_keys(passw)
    driver.find_element_by_id("login-button").click()
    time.sleep(10)
    driver.find_element_by_link_text(playlist).click()
    time.sleep(5)


    body = driver.find_element_by_xpath("//ol[@class= 'tracklist']")
    element = driver.find_element_by_xpath("//div[@class= 'PlaylistRecommendedTracks']")
    actions = ActionChains(driver)
    actions.move_to_element(element)
    actions.perform()

    time.sleep(12)

    label = {}
    number_of_tracks = driver.find_elements_by_xpath("//div[@class= 'tracklist-col name']")
    for items in number_of_tracks:
        Track = items.find_element_by_xpath(".//div[@class= 'tracklist-name ellipsis-one-line']").text
        Artist = items.find_element_by_xpath(".//span[@class= 'TrackListRow__artists ellipsis-one-line']").text
        label[Track] = Artist

    file = open("List.txt", "w", encoding='utf-8')
    for Tracks, Artists in label.items():
        labels = Tracks + " " + Artists + "\n"
        file.writelines(labels)

    time.sleep(5)
    driver.close()

# ___ EXECUTE SPOTIFY RENDER LIST. COMMENT OUT IF PRE RENDERED ___ #
# spotify_render_list()


# AMAZON CONVERSION #
# USERNAME AND PASSWORD HERE #
# EXAMPLE :
# uname = "username"
# password = "password"

uname = ""
passw = ""
time.sleep(10)

file = open("list.txt", "r", encoding='utf-8').read()
songs = file.split("\n")

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
    print("Redirected to Amazon SignIn!!!")
except:
    print("ERROR! The redirection was not successful!!!")
time.sleep(1)

# driver.execute_script('alert("Automation was not possible for 2step and OTP verification!!! Please log in within 1 minute and wait for automation to kick in!!! ");')
try:
    driver.find_element_by_id('ap_email').send_keys(uname)
    driver.find_element_by_id('continue').click()
    time.sleep(1)
    driver.find_element_by_id('ap_password').send_keys(passw)
    driver.find_element_by_id('signInSubmit').click()
except:
    "ERROR! Some problems with Driver or Browser caught. Please restart the program!!! "
    driver.close()

time.sleep(15)

target2 = "https://music.amazon.in/home"
try:
    driver.get(target2)
    print("Redirected to Amazon Music!!!")
except:
    print("ERROR! Redirection was not successful!!!")
time.sleep(2)

track_add_failed = []
track_add_successful = []
track_not_found = []
track_skipped = []

def add_to_playlist(song):
    global track_add_successful, track_add_failed, track_not_found, track_skipped
    time.sleep(1)
    driver.implicitly_wait(2)
    wait = WebDriverWait(driver, 6)
    try:
        wait_for_search = wait.until(EC.element_to_be_clickable((By.ID, 'searchMusic')))
        wait_for_search.click()
        wait_for_search.send_keys(song)
        try_blk1 = True
    except selenium.common.exceptions:  # .ElementClickInterceptedException as intercepted:
        try_blk1 = False


    if try_blk1 == True:
        try:
            wait_to_click = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'playerIconSearch')))
            wait_to_click.click()
            wait_to_click.click()
            try_blk2 = True
        except selenium.common.exceptions:
            try_blk2 = False


    else:
        print("ERROR: Operation on search element failed. Skipping current operation!!!")


    if try_blk2 is True:
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='titles']//h2[text()='Songs']")))
            print("Search result found for track -> " + song)
            song_found = True
            # print("Song found from 1st successful execution: " + str(song_found))

        except selenium.common.exceptions.TimeoutException:
            song_found = False
            # print("Song found from 1st exception: " + str(song_found))

        except TypeError:
            song_found = False
            print("Song found from 2nd exception: " + str(song_found))

    # print("Song found from check status: " + str(song_found))
    if song_found is True:

        try:
            dot_options = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class= 'horizontalTile TILE']//span[@class= 'playerIconDotMenu']")))
            for icon in dot_options:
                try:
                    icon.click()
                    break
                except:
                    continue

            menu = driver.find_element_by_xpath("//*[@id='contextMenuContainer']")
            hover = ActionChains(driver).move_to_element(menu)
            hover.perform()
            add_pl = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Add to playlist']")))
            add_pl.click()
            click_add = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class= 'playlistTitle' and text()= '"+playlist+"']")))
            click_add.click()

            try:
                skip = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class= 'buttonContainer']//button[text()= 'Skip']")))
                print("Track -> " + song + " already in your library. Skipping to the next!!")
                track_skipped.append(song)
                skip.click()
            except selenium.common.exceptions.TimeoutException:
                track_add_successful.append(song)
                print("Track -> " + song + " Added to Library: " + playlist)
                pass

        except selenium.common.exceptions:
            print("Unknown error has occurred during adding the song -> " + song)
            track_add_failed.append(song)
            pass

    else:
        print(song + " Not found. Skipping to the next!!! ")
        track_not_found.append(song)

try:
    driver.find_element_by_xpath("//div[contains(@class, 'icon-exit closeButton')]").click()
    print("Language Preference Popped up, and closed")
except selenium.common.exceptions.NoSuchElementException as e:
    print("Language Preference Popup didn't popup!!! Skipping to Playlist")

Playlist_Found = 0
Playlist_Created = 0

try:
    time.sleep(2)
    driver.find_element_by_link_text(playlist)
    print("Playlist -> "+ playlist + " found, Will skip to adding tracks!!!")
    Playlist_Found = 1

except selenium.common.exceptions.NoSuchElementException:
    print("Playlist not Found, Will be created")
    driver.find_element_by_id("newPlaylist").click()
    time.sleep(.5)
    driver.find_element_by_id("newPlaylistName").send_keys(playlist)
    time.sleep(.5)
    driver.find_element_by_class_name("buttonOption").click()
    time.sleep(2)
    print("playlist -> " + playlist + " not found. Hence created and will move to adding tracks!!! ")
    Playlist_Created = 1

def write_logs():
    global track_add_successful, track_add_failed, track_not_found, track_skipped

    time.sleep(0.5)

    file_success = open("Tracks_added.txt", "w", encoding='utf-8')
    for i in track_add_successful:
        name = str(i) + "\n"
        file_success.write(name)
    # file_success.close()

    time.sleep(0.5)

    file_failed = open("Tracks_failed.txt", "w", encoding='utf-8')
    for i in track_add_failed:
        name = str(i) + "\n"
        file_failed.write(name)
    # file_failed.close()

    time.sleep(0.5)

    file_skipped = open("Tracks_skipped.txt", "w", encoding='utf-8')
    for i in track_skipped:
        name = str(i) + "\n"
        file_skipped.write(name)
    # file_skipped.close()

    time.sleep(0.5)

    file_not_found = open("Tracks_not_found.txt", "w", encoding='utf-8')
    for i in track_not_found:
        name = str(i) + "\n"
        file_not_found.write(name)
    # file_not_found.close()

iteration_count = 0
if Playlist_Found or Playlist_Created is 1:
    time.sleep(2)
    for i in songs:
        iteration_count = iteration_count + 1
        if iteration_count == len(songs):
            "Possible tracks has added to Amazon Playlist. The program ends here"
            write_logs()
        else:
            add_to_playlist(i)

#     add_to_playlist("Something's Gotta Give Camila Cabello")




