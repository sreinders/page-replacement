# Page Replacement Algorithms

In a virtual memory based system that uses paging, page replacement algorithms help decide which pages will be swapped out when a new page needs to be allocated in memory. Created as an exercise to help commit page replacement concepts to memory, I will be implementing various page replacement algorithms. Ultimately once a sufficient number of algorithms have been implemented I hope to incorporate functionality that will help provide comparison between the different algorithms in terms of page fault rate.

## Usage Example


If no command line arguments or incorrect arguments are provided the relevant usage() function will be invoked providing instructions on how to execute the algorithms. Found below are descriptions of the required arguments which are used to set up a random sequence of page numbers references to test against the relevant replacement algorithm.

* npages = the number of pages in the virtual address space.
* nrefs  = the total number of page references in the address string.
* nframes = the number of frames in memory.

Clock page replacement:
```sh
python replacement-clock.py npages nrefs nframes
```

Least Recently Used page replacement:
```sh
python replacement-lru.py npages nrefs nframes
```

## Info

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/sreinders](https://github.com/sreinders)
