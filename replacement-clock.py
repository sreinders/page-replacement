import sys
import pagerefgen

def usage():
    print("""
        replacement-clock.py npages nrefs nframes

        This program generates a random sequence of page numbers and uses them
        to simulate the Clock page replacement algorithm.

        npages = the number of pages in the virtual address space
        nrefs  = the total number of page references in the address string
        nframes = the number of frames in memory
    """)

def clock_replacement(seq, frames):
    """implements the clock replacement algorithm, passed the generated reference string as argument"""
    print(seq)

    frames_total = frames # set to the global value of frames
    page_faults = 0 # amount of page faults that the reference string incurs against the algorithm
    clock_list = [] # acts similarly to an IVT, stores clock items as frames and allows us to find the page for a given frame in constant time
    clock_dict = {} # dictionary acts as a hashing function and allows us to find the corresponding frame for a given page number
    hand = 0 # used to iterate around the clock_list array

    for i in range(len(seq)): # for every page in the sequence reference
        curr_page = seq[i] # get the current page
        found = False # set found to False, used to determine execution flow

        if len(clock_list) < frames_total: # if the frames haven't been filled up yet...
            if curr_page in clock_dict: # if the current page is found within memory (check dict), set the status of the page to True
                frame = clock_dict[curr_page]
                clock_list[frame].status = True
                clock_dict[curr_page] = frame
                found = True
            if not(found): # if the current page is not found within memory, create a new page and add to next free frame
                clock_page = clock_item(curr_page, True)
                clock_list.append(clock_page)
                clock_dict[curr_page] = len(clock_list)-1
                page_faults += 1

        else: # if the frames have been filled up...
            if curr_page in clock_dict: # if the current page is found within memory (check dict), set the status of the page to True
                frame = clock_dict[curr_page]
                clock_list[frame].status = True
                clock_dict[curr_page] = frame
                found = True
            if not(found): # if the current page is not found within memory...
                while not(found): # while the current page has not been given a frame, find the next frame which is set as False
                    if clock_list[hand].status == False: # if current page in the frame is False, delete the old page then store and hash the new page to the frame
                        old_page = clock_list[hand].page
                        old_frame = clock_dict[old_page]
                        del clock_dict[old_page]
                        clock_dict[curr_page] = old_frame
                        clock_list[hand].page = curr_page
                        clock_list[hand].status = True
                        hand += 1
                        page_faults += 1
                        found = True
                        if hand == len(clock_list): # if the hand has reached midnight (the end of the array)...
                            hand = 0 # wrap the hand around to the beginning of the clock

                    else: # if the current frame is set as True, set it to False as it has had its chance!
                        clock_list[hand].status = False
                        hand += 1
                        if hand == len(clock_list):
                            hand = 0 # wrap the hand around to the beginning of the clock

    print(str(page_faults) + " page faults occured")
    prints(clock_list) # print the final state of the clock array
    print("The clock hand was pointing at a final position of " + str(hand))

def prints(clock_list):
    """takes the clock_list array as an argument and prints out the contents of the frames"""
    i = 0
    for item in clock_list:
        print("Frame #" + str(i) + " contains " + str(item.printer()))
        i += 1

class clock_item():
    """clock item class utilised by the clock replacement algorithm to store pages"""
    def __init__(self, page, status):
        self.page = page
        self.status = status

    def printer(self):
        return str("Page #" + str(self.page) + " which has a used status of " + str(self.status))

if __name__ == "__main__":
    if len(sys.argv) != 4: # [replacement-clock.py, arg1, arg2, arg3]
        usage()
        sys.exit(1)
    else:
        sequence = pagerefgen.generate(int(sys.argv[1]), int(sys.argv[2])) # argv[1] -> number of pages, argv[2] -> length of page reference string
        clock_replacement(sequence, int(sys.argv[3])) # argv[3] -> number of frames
