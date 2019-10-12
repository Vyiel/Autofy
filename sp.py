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
from termcolor import *
import colorama
colorama.init()


windows_location = str(os.environ['windir'])
rootdir = windows_location[:2]
driver_loc = rootdir+"\chromedriver"
# driver_loc is the variable that stores the current directory of chromedriver. You can change it at your will.

# ENTER YOUR USERNAME AND PASSWORDS FOR RESPECTIVE ACCOUNTS #

spotify_user_name = ""
spotify_password = ""
amazon_user_name = ""
amazon_password = ""
common_playlist = ""

def spotify_render_list():
    global spotify_user_name, spotify_password, common_playlist
    try:
        driver = webdriver.Chrome(executable_path=driver_loc)
        driver.implicitly_wait(10)
    except Exception:
        cprint("""Probably The chrome driver is not matched with your current Google Chrome version.
                Please update chrome to the latest version, and download and save the latest
                stable version of chromedriver on to the root of your Windows Installation!!! """, "red")
        time.sleep(2)
        driver.close()


    target = 'https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2Fbrowse%2Ffeatured'
    driver.get(target)

    driver.find_element_by_id("login-username").send_keys(spotify_user_name)
    driver.find_element_by_id("login-password").send_keys(spotify_password)
    driver.find_element_by_id("login-button").click()
    time.sleep(10)
    driver.find_element_by_link_text(common_playlist).click()
    time.sleep(5)

    driver.find_element_by_xpath("//ol[@class= 'tracklist']")
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

# ____________ CODE FOR SPOTIFY RENDITION ENDS ____________ #


# ____________ CODE FOR AMAZON MIGRATION _____________ #

track_add_failed = []
track_add_successful = []
track_not_found = []
track_skipped = []

def transfer_to_Amazon():
    global driver2, common_playlist, amazon_user_name, amazon_password

    time.sleep(10)

    file = open("List.txt", "r", encoding='utf-8').read()
    songs = file.split("\n")

    try:
        driver2 = webdriver.Chrome(executable_path=driver_loc)
        driver2.implicitly_wait(3)
    except Exception:
        print("""Probably The chrome driver is not matched with your current Google Chrome version.
                    Please update chrome to the latest version, and download and save the latest
                    stable version of chromedriver on to the root of your Windows Installation!!! """)

    target = 'https://www.amazon.in/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=inflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&switch_account='
    try:
        driver2.get(target)
        cprint("Redirected to Amazon SignIn!!!", "green")
    except:
        cprint("ERROR! The redirection was not successful!!!" "red")
        time.sleep(2)
        driver2.close()

    # driver.execute_script('alert("Automation was not possible for 2step and OTP verification!!! Please log in within 1 minute and wait for automation to kick in!!! ");')

    try:
        driver2.find_element_by_id('ap_email').send_keys(amazon_user_name)
        driver2.find_element_by_id('continue').click()
        time.sleep(1)
        driver2.find_element_by_id('ap_password').send_keys(amazon_password)
        driver2.find_element_by_id('signInSubmit').click()
    except:
        cprint("ERROR! Some problems with Driver or Browser caught. Please restart the program!!! ", "red")
        driver2.close()

    time.sleep(15)

    target2 = "https://music.amazon.in/home"
    try:
        driver2.get(target2)
        cprint("Redirected to Amazon Music!!!", "green")
    except:
        cprint("ERROR! Redirection was not successful!!!", "red")
        time.sleep(2)
        driver2.close()

    try:
        driver2.find_element_by_xpath("//div[contains(@class, 'icon-exit closeButton')]").click()
        cprint("Language Preference Popped up, and closed", "blue")
    except selenium.common.exceptions.NoSuchElementException:
        cprint("Language Preference Popup didn't popup!!! Skipping to Playlist", "blue")

    Playlist_Found = 0
    Playlist_Created = 0

    try:
        time.sleep(2)
        driver2.find_element_by_link_text(common_playlist)
        cprint("Playlist -> "+ common_playlist + " found, Will skip to adding tracks!!!", "green")
        Playlist_Found = 1

    except selenium.common.exceptions.NoSuchElementException:
        cprint("playlist -> " + common_playlist + " not found. Hence created and will move to adding tracks!!! ", "blue")
        driver2.find_element_by_id("newPlaylist").click()
        time.sleep(.5)
        driver2.find_element_by_id("newPlaylistName").send_keys(common_playlist)
        time.sleep(.5)
        driver2.find_element_by_class_name("buttonOption").click()
        time.sleep(2)
        Playlist_Created = 1

    iteration_count = 0

    if Playlist_Found or Playlist_Created is 1:
        time.sleep(2)
        for i in songs:
            iteration_count = iteration_count + 1
            if iteration_count == len(songs):
                cprint("Possible tracks has added to Amazon Playlist. The program ends here", "green")
                write_logs()
            else:
                add_to_playlist(i)

    #     add_to_playlist("Something's Gotta Give Camila Cabello")

def add_to_playlist(song):
    global track_add_successful, track_add_failed, track_not_found, track_skipped, common_playlist, driver2

    time.sleep(1)
    wait = WebDriverWait(driver2, 6)
    try:
        wait_for_search = wait.until(EC.element_to_be_clickable((By.ID, 'searchMusic')))
        wait_for_search.click()
        wait_for_search.send_keys(song)
        try_blk1 = True
    except selenium.common.exceptions:  # .ElementClickInterceptedException as intercepted:
        try_blk1 = False


    if try_blk1 is True:
        try:
            wait_to_click = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'playerIconSearch')))
            wait_to_click.click()
            wait_to_click.click()
            try_blk2 = True
        except selenium.common.exceptions:
            try_blk2 = False

    else:
        cprint("ERROR: Operation on search element failed. Skipping current operation!!!", "red")

    if try_blk2 is True:
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='titles']//h2[text()='Songs']")))
            cprint("Search result found for track -> " + song, "green")
            song_found = True
            # print("Song found from 1st successful execution: " + str(song_found))

        except selenium.common.exceptions.TimeoutException:
            song_found = False
            # print("Song found from 1st exception: " + str(song_found))

        except TypeError:
            song_found = False
            # print("Song found from 2nd exception: " + str(song_found))

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

            menu = driver2.find_element_by_xpath("//*[@id='contextMenuContainer']")
            hover = ActionChains(driver2).move_to_element(menu)
            hover.perform()
            add_pl = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Add to playlist']")))
            add_pl.click()
            click_add = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class= 'playlistTitle' and text()= '"+common_playlist+"']")))
            click_add.click()

            try:
                skip = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class= 'buttonContainer']//button[text()= 'Skip']")))
                cprint("Track -> " + song + " already in your library. Skipping to the next!!", "blue")
                track_skipped.append(song)
                skip.click()
            except selenium.common.exceptions.TimeoutException:
                track_add_successful.append(song)
                cprint("Track -> " + song + " Added to Library: " + common_playlist, "green")
                pass

        except selenium.common.exceptions:
            cprint("Unknown error has occurred during adding the song -> " + song, "red")
            track_add_failed.append(song)
            pass

    else:
        cprint(song + " Not found. Skipping to the next!!! ", "red")
        track_not_found.append(song)

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


# ____________ CODE FOR YOUTUBE SEARCH RESULT RENDITION _____________ #

youtube_links = []
def render_youtube_links():
    global driver3

    file = open("List.txt", "r", encoding='utf-8').read()
    songs = file.split("\n")

    try:
        driver3 = webdriver.Chrome(executable_path=driver_loc)
        driver3.implicitly_wait(3)
    except Exception:
        cprint("""Probably The chrome driver is not matched with your current Google Chrome version.
                    Please update chrome to the latest version, and download and save the latest
                    stable version of chromedriver on to the root of your Windows Installation!!! """, "red")

    target = "https://www.youtube.com/"
    try:
        driver3.get(target)
        cprint("Redirected to YouTube Search Page!!!", "green")
    except:
        cprint("ERROR! The redirection was not successful!!!" "red")
        time.sleep(2)
        driver2.close()

    time.sleep(5)

    for song in songs:
        cprint("Searching for track -> " + song, "blue")
        search_song(song)

    cprint("All possible links has been noted down", "green")

    # song = "Cycle Sabrina Claudio"
    # search_song(song)

def search_song(song):
    global driver3, youtube_links
    wait = WebDriverWait(driver3, 3)
    link = str()
    ytlf = bool
    time.sleep(1)
    driver3.find_element_by_id("search").send_keys(song)
    time.sleep(1)
    driver3.find_element_by_id("search-icon-legacy").click()
    time.sleep(1)
    try:
        ##### _________ CODE IF YOU WANT TO GRAB ALL THE FIRST AVAILABLE LINKS REGARDLESS OF MATCH _________ #####

        all_results = driver3.find_elements_by_xpath("//div[@id='dismissable' and @class='style-scope ytd-video-renderer']//a[@id='video-title']")
        cprint("The first link has been noted down! Might not be accurate", "yellow")
        cprint("The link has been grabbed from -> '" + str(all_results[0].get_attribute("title")) + "'", "green")
        link = all_results[0].get_attribute("href")
        youtube_links.append(str(link))
        print("______________________________________________________________")

        ##########################################################################################################

        ##### _________ CODE IF YOU WANT TO GRAB ALL THE FIRST AVAILABLE LINKS WHEN AND IF THERE IS A MATCH _________ #####

        # song_names = song.split(" ")
        # for words in song_names:
        #     try:
        #         print(words)
        #         results = driver3.find_elements_by_xpath("//a[@id='video-title' and contains(@title, '" + words + "')]")
        #         link = results[0].get_attribute("href")
        #         ytlf = True
        #         print(results[0].get_attribute("title"))
        #         break
        #     except:
        #         ytlf = False
        #         continue
        #
        # if ytlf is True:
        #     cprint("The Track -> " + song + " is possibly found and has been noted down", "green")
        # else:
        #     cprint("The Track -> " + song + " is not found and skipped to the next", "red")
        #
        # youtube_links.append(str(link))
        # print("______________________________________________________________")


        # ALSO BUGGY AT TIMES. USE WHATEVER MODULE YOU WANT
        ###################################################################################################################


    except selenium.common.exceptions:
        cprint("ERROR performing operation", "red")

    driver3.find_element_by_id('search').send_keys(Keys.CONTROL + "a")
    time.sleep(1)
    driver3.find_element_by_id('search').send_keys(Keys.DELETE)
    time.sleep(1)

    file = open("Youtube_links.txt", 'w', encoding = 'utf-8')
    for link in youtube_links:
        if len(link) >= 1:
            writable_link = str(link) + "\n"
            file.write(writable_link)


# ___________ CODE FOR YOUTUBE -> MP3 ____________ #

def yt2mp3():
    file = "Youtube_links.txt"
    ytdlroot = rootdir + "\ytdl\\"
    command = ytdlroot + "youtube-dl.exe -a " + file + " -x --audio-format mp3 --audio-quality 0"
    print(command)
    os.system(command)


# _________________ RUN SPECIFIC OR BATCH JOBS FROM HERE _________________ #


# spotify_render_list()
# # transfer_to_Amazon()
render_youtube_links()
# yt2mp3()