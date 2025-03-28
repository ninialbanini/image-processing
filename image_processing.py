import doctest 

def valid_int (s):
    '''(str) -> bool
    Takes a string as input and checks if any of its elements
    are not in the valid int list. Returns False if it is,
    or raises an AssertionError if it is not.
    
    >>> valid_int('25! 32')
    Traceback (most recent call last):
    AssertionError: Invalid value detected in image matrix.
    
    >>> valid_int('25 32')
    False
    
    >>> valid_int('13 13')
    False
    '''
    
    valid_int_val = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
    
    for elmt in s:
        if elmt not in valid_int_val:
            raise AssertionError("Invalid value detected in image matrix.")
        
    return False 
    
def is_valid_image(n_list):
    '''(list<list>) -> bool
    Takes a nested list as input and returns a bool
    indicating if nested list is a valid (non-compressed)
    list that contains integers from 0-255, and rows of the
    same length
    
    >>> is_valid_image([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    True
    
    >>> is_valid_image([[1, 3], [0, 0], [9, 8], [1]])
    False
    
    >>> is_valid_image([[],[]])
    False
    '''
    i = 0
    
    if len(n_list) == 0:
        return False
    
    for l in n_list:
        
        if len(l) == 0:
            return False
        
        for elmt in l:
            if type(elmt) != int or elmt < 0 or elmt > 255:
                return False 
        
        if l == n_list[-1]:
            if len(n_list[i]) == len(n_list[i-1]):
                break
            else:
                return False
        
        elif len(n_list[i]) == len(n_list[i+1]):
            i += 1
        
        else:
            return False
        
    return True

def is_valid_compressed_image(n_list):
    '''(list<list<str>>) -> bool
    Takes a nested list as input and returns a boolean indicating if
    input represents a valid compressed PGM image matrix. Compressed PGM
    image is one that contains only strings of the form 'AxB', where A is
    an integer between 0-255 and B is a positive integer. The sum of B values
    in each row must be the same.
    
    >>> is_valid_compressed_image([["0x0", "200x3"], ["111x3"], ["0x2", "200x1"], ["111x3"]])
    False
    
    >>> is_valid_compressed_image([["05", "200x256"], ["111x7"]])
    False
    
    >>> is_valid_compressed_image([["0x5", "20ax2"], ["111x7"]])
    False
    '''
    b_sum = -1
    new_b_sum = 0
    
    if len(n_list) == 0:
        return False 
        
    for r in n_list:
        if len(r) == 0:
            return False 
        for elmt in r: 
            if type(elmt) != str or elmt.count('x') != 1:
                return False
            
            x = elmt.find('x')
            a = elmt[:x]
            b = elmt[x+1:]
            
            if not (a.isdecimal() and b.isdecimal()):
                return False
            
            if int(a) < 0 or int(a) > 255 or int(b) <= 0:
                return False
            
            new_b_sum += int(b)
            
        if b_sum == -1: #checking if it's the first row
            first_b_sum = new_b_sum
            b_sum = 0
            
        elif new_b_sum != first_b_sum: #checking for all rows after the first to make sure they match
            return False
        
        new_b_sum = 0
            
    return True

def line_under_three(line, line_num, comp):
    '''(str, int, bool) -> NoneType
    Takes a line string from an image matrix, its corresponding
    line number and a boolean indicating whether it's a compressed
    image matrix or not. Returns nothing, but raises an AssertionError
    if it is deemed invalid. 
    
    >>> line_under_three('     P2\\n', 1, False)
    Traceback (most recent call last):
    AssertionError: PGM files must no spaces in line 1
    
    >>> line_under_three('25a 32', 2, False)
    Traceback (most recent call last):
    AssertionError: Invalid value detected in image matrix.
    
    >>> line_under_three('25 32', 2, True)
    
    '''
    if line_num == 1:
        if line.count(' ') != 0:
            raise AssertionError("PGM files must no spaces in line 1")
            
        line = line.strip('\n').split()
        if comp:
            if line[0] != 'P2C': 
                raise AssertionError("Compressed PGM files must start with P2C")
                
        elif line[0] != 'P2':
            raise AssertionError("PGM files must start with P2")
        
    elif line_num == 2:
        line = line.strip('\n')
        if line.count(' ') != 1 or valid_int(line):
            raise AssertionError("Too many spaces in line 2")
                    
    elif line_num == 3:    
        if line.count(' ') != 0:
            raise AssertionError("PGM files must no spaces in line 3")
            
        line = line.strip('\n').split()
        
        if line[0] != '255':
            raise AssertionError("Max value must be 255")
        
def row_count_calc(im_mat):
    ''' (list) -> int
    Takes an image matrix as input and returns the row count
    
    >>> row_count_calc([['11x5'], ['10x5'], ['255x5']])
    3
    
    >>> row_count_calc([['0x24'], ['0x1', '51x5', '0x1', '119x5', '0x1', '187x5', '0x1', '255x4', '0x1']])
    2
    
    >>> row_count_calc([['0x24']])
    1
    '''
    row_count = 0 
    
    for sublist in im_mat:
        row_count += 1
    return row_count

def load_regular_image(image):
    '''(str)-> list<list<int>>
    Takes a filename string as input and loads the image contained
    in file and returns it as a regular PGM image matrix. If it is not in PGM
    format at any point, an AssertionError is raised. 

    >>> load_regular_image("comp.pgm")
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 187, 187, 187, 187, 0, 255, 255, 255, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 255, 255, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0], [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    >>> fobj = open("invalid.6.pgm", "w")
    >>> fobj.write("P2\\n10 3\\n255\\n")
    12
    >>> load_regular_image("invalid.6.pgm")
    Traceback (most recent call last):
    AssertionError: Invalid image matrix.
    
    >>> load_regular_image('comp.pgm.compressed')
    Traceback (most recent call last):
    AssertionError: PGM files must start with P2
    '''
    im_mat = []
    line_num = 0
    row_count = 0
    
    pic = open(image, 'r')
    
    for line in pic:
        line_num += 1
        l = []  
        
        if line_num <= 3:
            line_under_three(line, line_num, False)
            if line_num == 2:
                line = line.strip('\n').split()
                width = line[0]
                height = line[1]
            continue 
        
        line = line.strip('\n').split()
        
        for elmt in line:
            if valid_int(elmt):
                raise AssertionError("Detected an invalid entry in the image matrix.")
            
            l.append(int(elmt))
        
        im_mat.append(l)
    
    pic.close()
    
    if not is_valid_image(im_mat):
        raise AssertionError("Invalid image matrix.")

    row_count = row_count_calc(im_mat)
    
    if len(im_mat[0]) != int(width) or row_count != int(height):
        raise AssertionError ("Column/and or row count does not match")
    
    return (im_mat)
    
def b_sum_calc(l):
    '''(list<str>) -> int
    Takes a list of strings as input, splits the string
    to find the b values and returns their sum. 
    
    >>> b_sum_calc(['0x1', '51x5', '0x1', '119x5', '0x1', '187x5', '0x1', '255x4', '0x1'])
    24
    
    >>> b_sum_calc(["0x5", "200x2"])
    7
    
    >>> b_sum_calc(['11x1', '0x2', '14x1', '0x1'])
    5
    '''
    
    b_sum = 0
    
    for elmt in l:
        x = elmt.find('x')
        b_val = elmt[x+1:]
        b_sum += int(b_val)
    
    return b_sum

def load_compressed_image(image):
    '''(str) -> list<list<str>>
    Takes a filename string of a compressed PGM image as input and
    returns the loaded file into a compressed image matrix. If at any
    point the resulting image matrix is an invalid compressed image format,
    then an AssertionError is raised.
    
    >>> load_compressed_image("comp.pgm.compressed")
    [['0x24'], ['0x1', '51x5', '0x1', '119x5', '0x1', '187x5', '0x1', '255x4', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x2', '255x1', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x4', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'], ['0x1', '51x5', '0x1', '119x5', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'], ['0x24']]
    
    >>> load_compressed_image('test.pgm.compressed')
    [['0x5', '200x2'], ['111x7']]
    
    >>> load_compressed_image('comp.pgm')
    Traceback (most recent call last):
    AssertionError: Compressed PGM files must start with P2C
    '''
    im_mat = []
    line_num = 0
    row_count = 0
    b_sum = 0
    b_val = 0
    
    pic = open(image, 'r')
    
    for line in pic:
        line_num += 1
        l = []  
        
        if line_num <= 3:
            line_under_three(line, line_num, True)
            if line_num == 2:
                line = line.strip('\n').split()
                width = line[0]
                height = line[1]
    
            continue
        
        line = line.strip('\n').split()
        
        for elmt in line:
            l.append((elmt))
        
        im_mat.append(l)
    
    pic.close()
        
    if not is_valid_compressed_image(im_mat):
        raise AssertionError("Invalid compressed image matrix.")
    
    row_count = row_count_calc(im_mat)
    b_sum = b_sum_calc(im_mat[0])
    
    if row_count != int(height) or b_sum != int(width):
        raise AssertionError("Row and/or column count do not match")
    
    return im_mat
  
def load_image(image):
    '''(str) -> list<list>
    Takes a filename string as input. Reads the first line and checks if
    first line is 'P2C' or 'P2' and returns a compressed PGM image or a
    a regular PGM image respectively. If it is neither, raises an AssertionError.

    >>> fobj = open("invalid_test.pgm", "w")
    >>> fobj.write("abc\\n30 6\\n259\\nabc133333x23 0x0x7\\n")
    32
    >>> fobj.close()
    >>> load_image("invalid_test.pgm")
    Traceback (most recent call last):
    AssertionError: Not a valid PGM or PGM compressed file
    
    >>> load_image("comp.pgm.compressed")
    [['0x24'], ['0x1', '51x5', '0x1', '119x5', '0x1', '187x5', '0x1', '255x4', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x2', '255x1', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x4', '0x1'], ['0x1', '51x1', '0x5', '119x1', '0x3', '119x1', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'], ['0x1', '51x5', '0x1', '119x5', '0x1', '187x1', '0x1', '187x1', '0x1', '187x1', '0x1', '255x1', '0x4'], ['0x24']]
    
    >>> load_image("comp.pgm")
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 187, 187, 187, 187, 0, 255, 255, 255, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 255, 255, 255, 0], [0, 51, 0, 0, 0, 0, 0, 119, 0, 0, 0, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0], [0, 51, 51, 51, 51, 51, 0, 119, 119, 119, 119, 119, 0, 187, 0, 187, 0, 187, 0, 255, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    '''
    
    pic = open(image, "r")
    pic_type = pic.read(3)
    pic.close()
    
    if 'P2C' in pic_type:
        return(load_compressed_image(image))
    
    elif 'P2' in pic_type:
        return(load_regular_image(image))
    
    else:
        raise AssertionError("Not a valid PGM or PGM compressed file") 

def save_regular_image(n_list, image_name):
    '''(list<list>, str) -> NoneType
    Takes a nested list and a image name string. Returns nothing but saves
    it in PGM format with the given image name. If the nested list is not a
    valid regular image matrix, an AssertionError is raised. 

    >>> save_regular_image([[0]*10, [255]*10, [0]*10], "test.pgm")
    >>> fobj = open("test.pgm", 'r')
    >>> fobj.read()
    'P2\\n10 3\\n255\\n0 0 0 0 0 0 0 0 0 0\\n255 255 255 255 255 255 255 255 255 255\\n0 0 0 0 0 0 0 0 0 0\\n'
    >>> fobj.close()
    
    >>> save_regular_image([], 'hi')
    Traceback (most recent call last):
    AssertionError: Cannot save image as it is not a valid PGM image.
    
    >>> save_regular_image([[10, 3, 2]*5, [1, 7, 9]*5], 'yay.pgm')
    >>> fobj = open('yay.pgm', 'r')
    >>> fobj.read()
    'P2\\n15 2\\n255\\n10 3 2 10 3 2 10 3 2 10 3 2 10 3 2\\n1 7 9 1 7 9 1 7 9 1 7 9 1 7 9\\n'
    >>> fobj.close()
    ''' 
    i = 0
    
    if not is_valid_image(n_list):
        raise AssertionError("Cannot save image as it is not a valid PGM image.")
        
        
    num_rows = len(n_list)
    num_cols = len(n_list[0])
    pgm_pic = open(image_name, "w")
    pgm_pic.write("P2\n")     
    pgm_pic.write(str(num_cols) + ' ' + str(num_rows))
    pgm_pic.write("\n255")
        
    for r in n_list:
        pgm_pic.write("\n")
            
        for elmt in r:
            if i == len(r)-1:
                pgm_pic.write(str(elmt))
                i = 0
            else: 
                pgm_pic.write(str(elmt) + ' ')
                i += 1
        
    pgm_pic.write("\n")     
    pgm_pic.close()        

def save_compressed_image(n_list, image_name):
    '''(list<list<str>>, str) -> NoneType
    Takes a nested list corresponding to a compressed image matrix and
    an image name string as input. Returns nothing but saves the nested list
    in compressed PGM format with the image name. If the nested list is an invalid
    compressed image matrix, raises an AssertionError. 
    
    >>> save_compressed_image([["0x5", "200x2"], ["111x7"]], "test.pgm.compressed")
    >>> fobj = open("test.pgm.compressed", 'r')
    >>> fobj.read()
    'P2C\\n7 2\\n255\\n0x5 200x2\\n111x7\\n'
    >>> fobj.close()
    
    >>> save_compressed_image([[]], 'yesss')
    Traceback (most recent call last):
    AssertionError: Cannot save image as it is not a valid compressed PGM image.
    
    >>> save_compressed_image([["0x3", "200x3"], ["111x6"], ["3x2", "5x1", "100x2", "255x1" ]], "new.pgm.compressed")
    >>> fo = open("new.pgm.compressed", "r")
    >>> fo.read()
    'P2C\\n6 3\\n255\\n0x3 200x3\\n111x6\\n3x2 5x1 100x2 255x1\\n'
    >>> fo.close()
    '''
    i = 0
    
    if not is_valid_compressed_image(n_list):
        raise AssertionError("Cannot save image as it is not a valid compressed PGM image.")
        
    num_rows = len(n_list)
    b_sum = b_sum_calc(n_list[0])   
    num_cols = b_sum
        
    pgm_pic = open(image_name, "w")
    pgm_pic.write("P2C\n")     
    pgm_pic.write(str(num_cols) + ' ' + str(num_rows))
    pgm_pic.write("\n255")
        
    for r in n_list:
        pgm_pic.write("\n")
            
        for elmt in r:
            if i == len(r)-1:
                pgm_pic.write(str(elmt))
                i = 0
                
            else: 
                pgm_pic.write(str(elmt) + ' ')
                i += 1
        
    pgm_pic.write("\n")     
    pgm_pic.close()


def save_image(n_list, image_name):
    ''' (list<list>, str) -> NoneType
    Takes a nest list and an image name as a string as input. Reads the
    type of elements in the nested list and determines if it's a regular
    PGM image matrix with ints or a compressed PGM image matrix with strings.
    If it is anything else, then an AssertionError is raised.

    >>> save_image([["0x5", "200x2"], ["111x7"]], "test.pgm.compressed")
    >>> fobj = open("test.pgm.compressed", 'r')
    >>> fobj.read()
    'P2C\\n7 2\\n255\\n0x5 200x2\\n111x7\\n'
    
    >>> save_image([], 'new.pgm')
    Traceback (most recent call last):
    AssertionError: Length of lists cannot be 0
    
    >>> save_image([[10, 3, 2]*5, [1, 7, 9]*5], 'yay.pgm')
    >>> fobj = open('yay.pgm', 'r')
    >>> fobj.read()
    'P2\\n15 2\\n255\\n10 3 2 10 3 2 10 3 2 10 3 2 10 3 2\\n1 7 9 1 7 9 1 7 9 1 7 9 1 7 9\\n'
    >>> fobj.close()
    '''
    
    if len(n_list) == 0 or len(n_list[0]) == 0:
        raise AssertionError("Length of lists cannot be 0")
    
    if type(n_list[0][0]) == int:
        pgm_pic = save_regular_image(n_list, image_name)
    
    elif type(n_list[0][0]) == str:
        pgm_pic = save_compressed_image(n_list, image_name)
    
    else:
        raise AssertionError("Sorry this is an invalid image type")
    

def invert(im_mat):
    '''(list<list<int>>)-> list<list<int>>
    Takes a nested list of ints corresponding to a regular PGM image matrix as
    input. Returns the inverted matrix, without changing the original. If the nested
    list is an invalid PGM matrix, an AssertionError is raised. 
    
    >>> image = [[0, 100, 150], [200, 200, 200], [255, 255, 255]]
    >>> invert(image)
    [[255, 155, 105], [55, 55, 55], [0, 0, 0]]
    
    >>> image = []
    >>> invert(image)
    Traceback (most recent call last):
    AssertionError: Unable to invert image as image matrix is invalid
    
    >>> invert([[255, 149, 0]])
    [[0, 106, 255]]
    '''
    
    inverted_im_mat = []
    
    if not is_valid_image(im_mat):
        raise AssertionError("Unable to invert image as image matrix is invalid")
    
    for r in im_mat:
        new_r = []
            
        for e in r:
            e = 255 - e
            new_r.append(e)
            
        inverted_im_mat.append(new_r)
            
    return inverted_im_mat
        
        
def flip_horizontal(im_mat):
    '''(list<list<int>>)-> list<list<int>>
    Takes a regular image matrix as input and returns a copied version
    of the image matrix flipped horizontally. If the image matrix is invalid
    an AssertionError is raised. 
    
    >>> image = [[1, 2, 3, 4, 5], [0, 0, 5, 10, 10], [5, 5, 5, 5, 5]]
    >>> flip_horizontal(image)
    [[5, 4, 3, 2, 1], [10, 10, 5, 0, 0], [5, 5, 5, 5, 5]]
    
    >>> flip_horizontal([])
    Traceback (most recent call last):
    AssertionError: Unable to flip image horizontally as image matrix is invalid
    
    >>> flip_horizontal([[5, 6, 7, 8], [9, 10, 11, 12], [100, 101, 102, 103], [104, 250, 255, 40]])
    [[8, 7, 6, 5], [12, 11, 10, 9], [103, 102, 101, 100], [40, 255, 250, 104]]
    '''
    
    horizontal_im_mat = []
    
    if not is_valid_image(im_mat):
        raise AssertionError("Unable to flip image horizontally as image matrix is invalid")
    
    for r in im_mat:
        new_r = []
        i = 0
        for e in r:
            new_e = str(r[i-1])
            new_r.append(int(new_e))
            i -= 1
            
        horizontal_im_mat.append(new_r)
            
    return horizontal_im_mat 
        

def flip_vertical(im_mat):
    '''(list<list<int>>)-> list<list<int>>
    Takes a regular image matrix as input and returns a copied version
    of the image matrix flipped vertically. If the image matrix is invalid
    an AssertionError is raised. 

    >>> image = [[1, 2, 3, 4, 5], [0, 0, 5, 10, 10], [5, 5, 5, 5, 5]]
    >>> flip_vertical(image)
    [[5, 5, 5, 5, 5], [0, 0, 5, 10, 10], [1, 2, 3, 4, 5]]
    
    >>> image = [[1, 2, 3, 4, 5], [0, 0, 5, 10, 10], [10, 9, 8, 7, 7], [5, 5, 5, 5, 5]]
    >>> flip_vertical(image)
    [[5, 5, 5, 5, 5], [10, 9, 8, 7, 7], [0, 0, 5, 10, 10], [1, 2, 3, 4, 5]]

    >>> flip_vertical([[-1]])
    Traceback (most recent call last):
    AssertionError: Unable to flip image vertically as image matrix is invalid
    ''' 
    vertical_im_mat = []
    i = 0
    
    if not is_valid_image(im_mat):
        raise AssertionError("Unable to flip image vertically as image matrix is invalid") 
        
    for line in im_mat:
        new_line = [] 
        line = im_mat[i-1]
        i-=1
            
        for e in line:
            new_e = e
            new_line.append((new_e))
            
        vertical_im_mat.append(new_line)
            
    return vertical_im_mat 
    
def crop(im_mat, start_r, start_c, row, col):
    '''(list<list<int>>, int, int, int, int) -> list<list<int>>
    Takes a regular image matrix as input, a starting row and column
    index, and the desired ending indices of the row and column for the
    cropped image. Returns a copied cropped image matrix. If the input
    image matrix is invalid, an AssertionError is raised.

    >>> crop([[5, 5, 5], [5, 6, 6], [6, 6, 7]], 1, 1, 2, 2)
    [[6, 6], [6, 7]]
    
    >>> crop([[0, 1], [1, 0], [0,1]], 0, 0, 1, 1)
    [[0]]
    
    >>> crop([[2, 6, 1, 0], [4, 3, 1, 3], [7, 29, 32, 42]], 2, 2, 1, 2)
    [[32, 42]]
    '''
    cropped_im = []
    
    if not is_valid_image(im_mat) or row == 0 or col == 0:
        raise AssertionError("Unable to crop image as image matrix is invalid")
    
    for i in range(row):
        new_line = []
        og_c = start_c 
            
        for j in range(col):
            line = im_mat[start_r][start_c]
            new_e = line
            new_line.append((new_e))
            start_c += 1
                
        cropped_im.append(new_line)
        start_c = og_c
        start_r += 1 
            
    return cropped_im 
            

def find_end_of_repetition(l_int, start_i, target):
    '''(list<int>, int, int) -> int
    Takes a list of integers, an integer corresponding to the
    starting index and an integer for the target number as input.
    Looks through the list at the starting index and returns the
    index of the last consecutive occurence of the target number. 

    >>> find_end_of_repetition([1, 2, 3, 4, 5, 6, 7], 6, 7)
    6
    >>> find_end_of_repetition([5, 3, 5, 5, 5, -1, 0], 2, 5)
    4
    >>> find_end_of_repetition([11, 11, 11, 11, 11], 0, 11)
    4
    '''  
    if start_i < 0 or target < 0:
        return("Integers must be non-negative")
    
    for i in range(len(l_int)):
        if l_int[start_i] == target:
            if start_i != (len(l_int)-1):
                start_i += 1
            else:
                return start_i   
        else:
            return (start_i - 1)

def compress(im_mat):
    '''(list<list<int>>) -> list<list<str>>
    Takes a non-compressed image matrix as input and returns
    its respective compressed image matrix. If the matrix is invalid
    an AssertionError is raised.

    >>> compress([[11, 11, 11, 11, 11], [10,10,10,10,10], [255, 255, 255, 255, 255]])
    [['11x5'], ['10x5'], ['255x5']]
    
    >>> compress([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]])
    [['1x1', '2x1', '3x1', '4x1', '5x1'], ['6x1', '7x1', '8x1', '9x1', '10x1'], ['11x1', '12x1', '13x1', '14x1', '15x1']]
    
    >>> compress([[1, 1, 3, 3, 4], [100, 3, 3, 3, 100], [11, 0, 0, 14, 0]])
    [['1x2', '3x2', '4x1'], ['100x1', '3x3', '100x1'], ['11x1', '0x2', '14x1', '0x1']]
    '''
    
    if not is_valid_image(im_mat):
        raise AssertionError("Unable to compress image as image matrix is invalid")
    
    compressed = []
        
    for sublist in im_mat:
        elmt_adds = []
        i = 0
            
        while i < len(sublist):
            reps = find_end_of_repetition(sublist, i, sublist[i]) - i + 1
            elmt_adds.append(str(sublist[i])+'x'+str(reps))
            i += reps 
            
        compressed.append(elmt_adds)
            
    return compressed


def decompress(com_mat):
    '''(list<list<str>>) -> list<list<int>>
    Takes a compressed image matrix as input and returns
    its respective decompressed image matrix. If the matrix is invalid
    an AssertionError is raised.
    
    >>> decompress([['1x2', '3x2', '4x1'], ['100x1', '3x3', '100x1'], ['11x1', '0x2', '14x1', '0x1']])
    [[1, 1, 3, 3, 4], [100, 3, 3, 3, 100], [11, 0, 0, 14, 0]]
    
    >>> decompress([['11x5'], ['10x5'], ['255x5']])
    [[11, 11, 11, 11, 11], [10, 10, 10, 10, 10], [255, 255, 255, 255, 255]]
    
    >>> decompress([['x']])
    Traceback (most recent call last):
    AssertionError: Invalid PGM compressed image matrix.

    '''
    
    if not is_valid_compressed_image(com_mat):
        raise AssertionError("Invalid PGM compressed image matrix.")
    
    decompressed = []
        
    for sublist in com_mat:
        elmt_adds = []
        a_val = 0
        b_val = 0
            
        for elmt in sublist:
            x_spot = elmt.find('x')
                
            a_val = int(elmt[:x_spot])
            b_val = int(elmt[x_spot+1:])
                            
            for i in range (b_val):
                elmt_adds.append(a_val) 
                
        decompressed.append(elmt_adds)
        
    return decompressed

        
def process_command(command):
    '''(str) -> NoneType
    Takes a command string as input. Follows the command if they are one
    of the following accepted commands: 'LOAD', 'SAVE', 'INV', 'FH', 'FV',
    'CR', 'CP', 'DC', which correspond to their respective functions above.
    If it is anything else, an AssertionError is raised. 
    
    >>> process_command("LOAD<comp.pgm> CP DC INV INV          SAVE<comp2.pgm>")
    >>> image = load_image("comp.pgm")
    >>> image2 = load_image("comp2.pgm")
    >>> image == image2
    True

    >>> process_command("LOAD<comp.pgm> CR<1,2,3> DC INV SAVE<comp2.pgm>")
    Traceback (most recent call last):
    AssertionError: Crop needs 4 arguments.
    
    >>> process_command("LOAD<> CR<1,2,3> DC INV SAVE<comp2.pgm>")
    Traceback (most recent call last):
    AssertionError: Cannot load an empty string filename
    '''   
    command = command.split()
    
    for elmt in command:
        
        if 'LOAD' in elmt:
            name_i = elmt.find('<') + 1
            im_name = elmt[name_i:-1]
            if im_name == '':
                raise AssertionError("Cannot load an empty string filename")
            image = load_image(im_name)
            
        elif elmt == 'CP':
            image = compress(image)
        
        elif elmt == 'INV':
            image = invert(image)
        
        elif elmt == 'FH':
            image = flip_horizontal(image)
        
        elif elmt == 'FV':
            image = flip_vertical(image)
        
        elif 'CR' in elmt:
            if '<' not in elmt and '>' not in elmt:
                raise AssertionError("Crop needs the following arguments : <x, y, h, w>")
            
            start = elmt.find('<')
            end = elmt.find('>')
            
            if elmt[:start] != 'CR' or elmt[end+1:] != '':
                raise AssertionError('invalid command detected')
            
            crop_indices = elmt[3:-1]
            crop_indices = crop_indices.split(',')
            
            if len(crop_indices) != 4:
                raise AssertionError("Crop needs 4 arguments.")
            
            image = crop(image, int(crop_indices[0]), int(crop_indices[1]), int(crop_indices[2]), int(crop_indices[3]))
        
        elif elmt == 'DC':
            image = decompress(image)
        
        elif 'SAVE' in elmt:
            name_i = elmt.find('<') + 1
            new_im_name = elmt[name_i:-1]
            if new_im_name == '':
                raise AssertionError("Cannot save an image with an empty string filename")
            image = save_image(image, new_im_name)
        
        else:
            raise AssertionError("Only the following commands are acceptable, \
'LOAD', 'SAVE', 'INV', 'FH', 'FV', 'CR', 'CP', 'DC'")
        

#if __name__ == "__main__":
    #doctest.testmod()