import random, shutil, os.path

filename     = "test"
extension    = "txt"
mutations    = 35600
count        = 0

def write_file(position, char):
    
    f = open("C:\\Python26\\pyfuzz\\test_cases\\%s.%s" % (str(count), extension), "r+b")
    f.seek(position,0)
    f.write(char)
    f.close()
    
def morph_file():
    
    position = random.randrange(file_length)
    bytes_to_morph = random.randint(1,4)
    shutil.copy2("C:\\Python26\\pyfuzz\\samples\\%s.%s" % (filename, extension), "pyfuzz/test_cases/%s.%s" % (str(count), extension))
    print "File %d" % count
    print "Start at byte %d" % position
    print "Morphing %d bytes\n" % bytes_to_morph
    for i in range(bytes_to_morph):
        write_file(position, chr(random.randrange(256)))
        position += 1
        if position >= file_length:
            break

file_length  = os.path.getsize("C:\\Python26\\pyfuzz\\samples\\"+filename+"."+extension)

while count != mutations:
    morph_file()
    count += 1
