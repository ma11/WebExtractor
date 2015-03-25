# WebExtractor

You may be here just to know how to use it, so do not read everything and directly jump to part
        IV) How to use

You also can read everything.

## Summary

    1, Generalities
    2, Features
    3, Coding Style
    4, How to use


## I) Generalities

This tool extract lines from web sites like danstonchat.com or viedemerde.com to print it on screen.
These textual-blog-like website do not really need a whole complicated internet browser to display information, it's just few text lines...

The present project propose a tool to download webpages from these kinf of website, parse it to extract usefull information, and then print it on screen.


## II) Features

### IIA) Existing features

* Print N last posts
* Print N random posts
* Print last post ID
* Doc generation by doxygen (see IV) How to use)

Where N is user define.

These feature are only available for some website, and the software tuning for these website are hardcoded (if you want to add more websites, you'll have to edit the code).
The available websites so on are:
    * http://danstonchat.com
    * http://viedemerde.fr
    * http://chucknorrisfact.fr
    * http://pebkac.fr


### IIB) Features that could be cool to have

For the moment, the tool is mainly working on the same way as the website does: if there is a latest post page, then the tool can print the latest post,
    if there is a random page, then the tool can print random posts,... etc
It could be cool to have features totally disconnected from website behavior, like printing posts that contain a certain expression, or posts that are related to an event
    or posted at a certain date.

Moreover, the project could introduce more intelligency: it could be cool to save last posts read for every website, and have an option (or a default behavior) that 
    consists in printing only new unseen posts.

To have a summerize, features that are cool but not yet implemented are:
    * Save last seen posts and print only new unseen posts
    * Print posts containing a certain expression
    * Print a list of post related to each other (graph proximity, social-like intelligency,...)
    * Print list of posts uploaded at a given date
    * Print list of post from a given user


##III) Coding Style

This program is python-one-file-only. Everything is described into one single file. Hence, if the user wants a very specific behavior, he has to go into the code.
It could be a good idea to change this, specially for the definition of html parsers: the user could define in a config file the tags used for extracting
    data post, or ID post,... So that the maintainer doesn't have to code a big python script containing all textual-blog-like website.
Only one person wrote the code. So the code is given as-it-is, without specific defined coding style.


##IV) How to use

###IV_A) Use of Software

Basicaly, you can read the help by:
```>> blogPrint --help```

And it will print what you need to know.

Basically, you can use the software without any option, and it will (should) print last 2 blog items from http://danstonchat.com (french website) - only if default behavior has not been changed...
You can change the behavior by using options: see >>blogPrint --help

If there is an error:
    1, Check you internet connection
    2, Check you powered your computer
    3, Check you correctly plug the keyboard
    4, Too bad... Send email to AUTHORS


###IV_B) Generating documentation

You can generate documentation using:

```>> make doxygen-doc```
