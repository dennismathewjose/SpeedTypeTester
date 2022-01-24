import curses
from curses import wrapper
import time
import random

#introduction screen
def intro(stdscr):

	stdscr.clear()
	stdscr.addstr("Welcome to basic speed typer test.\n You have 60 seconds to type the text. \nYour typing speed will be calculated by the number of words you typed in 60 seconds",curses.color_pair(3))
	stdscr.addstr(5,0,"\nPress any key to continue.\nPress esc to exit the program",curses.color_pair(3))
	key = stdscr.getkey()

	
#function to load random texts from a set of texts
def load_random_text(stdscr):
	with open("wpm_texts.txt", "r") as f:
		texts=f.readlines()
		return random.choice(texts).strip()


#function to overwrite the original text. 
def text_overlay(stdscr, target, current, Time, wpm=0):

	stdscr.addstr(target)
	stdscr.addstr(4,0,f"WPM : {wpm}") #to show the status of words per minute.
	stdscr.addstr(4,10,f"Time Left : {61-Time}") #to show the status of time.
	
     
     #enumerate function iterates i through the index of current and value at the i'th index.
	for i,char in enumerate(current):
		#if counter!=0:
		check_char = target[i]
		if char == check_char:
			color = curses.color_pair(1) # if the letters are correctly typed the status will be green
		else:
			color = curses.color_pair(2) #if any character goes wrong the letter will be in red.
		stdscr.addstr(0,i,char, color)


def wpm_test(stdscr):

	target = load_random_text(stdscr)
	current = []
	wpm=0 #inital words per minute
	start_time = time.time() #initial time.
	stdscr.nodelay(True) # to run the time and decrease the wpm if there is delay

	while True:

		elapsed_time = max(time.time() - start_time, 1) #start_time and time.time() will be same at an instant so inorder to remove the zeroDivison Error we take the maximum.

		time_left = int(elapsed_time)

		if time_left - 62 == 0:
			stdscr.nodelay(False) #do not wait for getkey status and break from the loop.
			break
        
        #calculating words per minute is done by : calculating the number of characters typed in x minutes divided by 5(5 is taken as the avg length of a word.)
		wpm = round((len(current)/(elapsed_time/60))/5)

		stdscr.clear()
		text_overlay(stdscr,target,current,time_left, wpm)
		stdscr.refresh()

		if "".join(current) == target:
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

		
		if ord(key) == 27:
			break
		
		if key in ("KEY_BACKSPACE", '\b', '\x7f'):  #value of backspace keys in different systems
			if len(current) > 0:
				current.pop()
		elif len(current) < len(target):
			current.append(key)
	return wpm

#main function
def main(stdscr):
	stdscr.clear()
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_YELLOW)

	intro(stdscr)

	while True:
		words=wpm_test(stdscr)
		stdscr.addstr(6,0,f"Your average typing speed is {words} words per minute.\nDo you wish to continue!!")
		key = stdscr.getkey()
		if ord(key) == 27:
			break

wrapper(main)
