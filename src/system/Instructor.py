from sys import exit


def main(man_page_name):
    """
    Main process for Instructor
    :return:
    """
    try:
        if man_page_name is None:
            # Read all the manual pages
            print("Kaster Password Vault's help")
            print()
            man_pages = ["man_generic.txt", "man_std.txt", "man_lw.txt", "man_gen.txt", "man_vault.txt"]
            for man in man_pages:
                main(man)
                input()
            del man, man_pages
        else:
            # Read specified manual page
            f = open("manual/" + man_page_name, "r")
            f_content = f.read()
            f.close()
            print(f_content)
            del f, f_content
    except KeyboardInterrupt:
        exit(0)
