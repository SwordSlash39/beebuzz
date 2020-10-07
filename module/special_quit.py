import sys, time
start = time.time()

def quit(txt: str="Finished code with runtime {} seconds"):
    if "{" in txt and "}" in txt:
        try:
            print(txt.format(round(time.time() - start, 1)))
            sys.exit()
        except KeyError:
            raise KeyError("Please put nothing inbetween the \"{\" and the \"}\"")
    else:
        raise SyntaxError("Need to include \"{}\"!")