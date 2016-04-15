import sys
import pagerefgen

def usage():
    print("""
        replacement-lru.py npages nrefs nframes

        This program generates a random sequence of page numbers and uses them
        to simulate the LRU page replacement algorithm.

        npages = the number of pages in the virtual address space
        nrefs  = the total number of page references in the address string
        nframes = the number of frames in memory
    """)

def lru_replacement(seq, frames):
    """implements the least recently used replacement algorithm, passed the generated reference string as argument"""
    print(seq)

    frames_total = frames # set to the global value of frames
    double_linked = DoubleList(frames_total) # create object of doubly linked list

    for i in range(len(seq)): # for every page in the sequence reference
        new_page = seq[i]
        double_linked.add(new_page)

    print(str(double_linked.page_faults) + " page faults occured") # print the amount of page faults that have occured
    double_linked.show() # print the final state of the lru algorithm

class Node():
    """ node class utilised by doubly list in lru replacement algorithm """
    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next

    def __str__(self):
        return str(" #" + str(self.data))

class DoubleList():
    """ doubly list utilised in lru replacement algorithm, avoids excessive search for precedessor node """
    def __init__(self, frames):
        self.head = None
        self.tail = None
        self.list = [] # list acts as an IVT, is an array of frames which store references to the nodes - frame->page
        self.dict = {} # dictionary acts as a hashing function and allows us to find page->frame
        self.capacity = frames # set to passed argument which has global value of frames
        self.page_faults = 0 # identifies the amount of page faults that the reference string incurs against the algorithm

    def add(self, value):
        """ adds the value (page) to the doubly list if it isn't already contained within, otherwise calls move method which deals with pages that are already cached/stored """
        if len(self.dict) >= self.capacity: # if memory is full...

            if value in self.dict: # if the value is already in memory swap it to the end of doubly list
                self.move(value) # call move method which determines specific case

            else: # if the value isn't already in memory, put LRU value at end of doubly list and remove the first item
                new_node = Node(value, None, None)
                tmp_frame = self.dict[self.head.data] # get frame of current head node from Dict
                del self.dict[self.head.data] # delete link between the current head (LRU value) page and it's frame in Dict
                self.dict[value] = tmp_frame # update Dict
                self.list[tmp_frame] = new_node # point the frame to the new_node in IVT
                self.head = self.head.next # fix the head node by pointing to next in line, set its prev value to None
                self.head.prev = None
                self.tail.next = new_node # set the current tail to point next to new_node
                self.tail.next.prev = self.tail
                self.tail = new_node # set new_node to be new tail
                self.page_faults += 1

        else:  # if memory isn't full, add the item
            if value in self.dict: # if the value is already in memory, swap to end of doubly list
                self.move(value) # call move method which determines specific case

            else:
                new_node = Node(value, None, None)
                if self.head is None: # if the memory is empty, set new_node as head and tail
                    self.head = self.tail = new_node
                    self.list.append(new_node) # add new_node to IVT
                    self.dict[value] = len(self.list)-1 # update Dict

                else: # if the memory is partially full, set new_nodes prev/next to suit it being the new tail
                    new_node.prev = self.tail
                    new_node.next = None
                    self.dict[value] = len(self.list) # update Dict
                    self.list.append(new_node) # add new_node to IVT
                    self.tail.next = new_node # set current tail to point to new_node, then set new_node as the new tail
                    self.tail = new_node
                self.page_faults += 1

    def move(self, value):
        """ move the value (page) from the appropriate spot in the doubly list to the most recently used area (end) """
        if self.tail.data == value: # if the tail is the node to be moved... dont move it
            pass
        else:
            tmp_frame = self.dict[value]
            tmp_node = self.list[tmp_frame] # get the node to be moved
            del self.dict[tmp_node.data] # delete its link from Dict

            if tmp_node.prev is None: # if the node is the head node, move the head along
                self.head = self.head.next
                self.head.prev = None
            else: # otherwise it is a node in between, update the prev and next nodes
                tmp_node.prev.next = tmp_node.next
                tmp_node.next.prev = tmp_node.prev

            self.tail.next = tmp_node # set the tail to point to the moved node
            tmp_node.prev = self.tail
            self.tail = tmp_node
            self.tail.next = None
            self.dict[value] = tmp_frame # update Dict

    def show(self):
        """ loops through the doubly list and displays the page values in order of the nodes in the list """
        temp = self.head
        while(temp is not None):
            print("Page" + str(temp) + " is contained within Frame #" + str(self.dict[temp.data]))
            temp = temp.next

if __name__ == "__main__":
    if len(sys.argv) != 4: # [replacement-lru.py, arg1, arg2, arg3]
        usage()
        sys.exit(1)
    else:
        sequence = pagerefgen.generate(int(sys.argv[1]), int(sys.argv[2])) # argv[1] -> number of pages, argv[2] -> length of page reference string
        lru_replacement(sequence, int(sys.argv[3])) # argv[3] -> number of frames
