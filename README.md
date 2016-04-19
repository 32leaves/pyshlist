# Introduction
This is a quick hack I put together to manage my wishlist of things I'd like to buy. Its main feature is to produce a graph plotting the wishlist items in desirability over urgency. The desirability rating results from a pair-wise comparison of wishlist items.

***HERE BE DRAGONS*** This is a quick hack and by no means good quality stuff. It get's the job done though.

# Installation
    git clone https://github.com/32leaves/pyshlist.git
    python setup.py install

# Quickstart
    # add a few items to a new database (pyslist addg opens a GUI for adding an item)
    pyshlist quickstart.json add --name Milk --price 2.99 --due 2016-04-30 --category food
    pyshlist quickstart.json add --name Honey --price 1.99 --due 2016-04-30 --category food
    pyshlist quickstart.json add --name Bread --price 0.99 --due 2016-04-26 --category food
    pyshlist quickstart.json add --name Beer --price 4.99 --due 2016-04-20 --category food

    # opens a TKinter GUI to compare the wishlist items
    pyshlist quickstart.json rate
![Rating wishlist items](/doc/rate_screenshot.png?raw=true)

    # draw the plot
    pyshlist quickstart.json plot --output quickstart.png
    
![Resulting plot](/doc/quickstart.png?raw=true)
    
# Usage
    $ pyshlist --help
    Usage: pyshlist-script.py [OPTIONS] FILE COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    add     Adds an item to the wishlist
    addg    Opens a GUI to add a new purchase to the list
    dump    Prints the wishlist
    plot    Creates the purchase scatter plot
    rate    Rate items regarding desirability (GUI only)
    remove  Removes an item from the wishlist
