def main(man_page_name):
    """
    Main process for Instructor
    :return:
    """
    if man_page_name is None:
        # Read all the manual pages
        man_pages = ["man_generic.txt", "man_lw.txt"]
        for man in man_pages:
            f = open("manual/" + man, "r")
            f_content = f.read()
            f.close()
            print(f_content)
            del f
        del man, man_pages, f_content
    else:
        # Read specified manual page
        f = open("manual/" + man_page_name, "r")
        f_content = f.read()
        f.close()
        print(f_content)
        del f, f_content
