import shutil

def unix2dos( file ):            
    infile = open(file,'r') 
    outfile = open( 'dos_' + file, 'w') 
    for line in infile: 
         line = line.rstrip() + '\r\n' 
         outfile.write(line) 
    infile.close() 
    outfile.close()         
    shutil.move('dos_' + file, file) 

def dos2unix( file ): 
    text = open(file, 'rb').read().replace('\r\n', '\n')
    open(file, 'wb').write(text)
