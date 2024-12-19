lines = Queue(1)
count = Queue(1)

def read(file):
    try:
        for line in file:
            lines.put(line)
    finally:
        lines.put(None)
    print(count.get())

def write(file):
    n = 0
    while 1:
        line = lines.get()
        if line is None:
            break
        file.write(line)
        n += 1
    count.put(n)

if __name__ == "__main__":
    import io
    input_file = io.StringIO("line1\n\line2\nAnother test line\n")
    output_file = sys.stdout
    reader = Thread(target=read, args=(input_file,))
    writer = Thread(target=write, args=(output_file,))
    reader.start() #START

    writer.start()
    reader.join()
    writer.join()
    #STOP
    print(output_file.getvalue())