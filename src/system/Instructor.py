from sys import exit
import logging


def main(man_page_name):
    """
    Main process for Instructor
    :return:
    """
    __process__ = "Instructor.py (main())"

    logging.basicConfig(filename="%s" % program_file_dir + "/log.dat",
                        format="[%(asctime)s] %(message)s",
                        datefmt="%s %s" % (time_format, date_format),
                        level=logging.INFO)

    try:
        if man_page_name is None:
            # Read all the manual pages
            print("Kaster Password Vault's help")
            print()
            man_pages = ["man_generic.txt", "man_lw.txt", "man_gen.txt", "man_vault.txt"]
            for man in man_pages:
                main(man)
                input()
            del man, man_pages
        else:
            # Read specified manual page
            try:
                f = open("manual/" + man_page_name, "r")
            except FileNotFoundError:
                logging.error("FATAL:%s: Couldn't find manual page (%s)" % (__process__, man_page_name))
                exit(1)
            f_content = f.read()
            f.close()
            print(f_content)
            del f, f_content
    except KeyboardInterrupt:
        logging.info("INFO:%s: Keyboard interrupted" % __process__)
        exit(0)
