def main():
    """
    Primary function of the program. Includes user interface.
    """
    coordinates = {} # Global variable
    # User input
    colour_list= {"BLANCO":"255 255 255","NEGRO":"0 0 0","MAGENTA":"255 0 255","AMARILLO":"255 255 0","ROJO":"255 0 0","VERDE":"0 255 0","AZUL": "0 0 255"}
    final_name = input ("Ingrese del nombre del archivo sin extencion: ")
    while True:
        size_x = input("Ingrese el tamaño en x: ")
        if size_x.isdigit():
            size_x = int(size_x)
            break
    while True:
        size_y = input("Ingrese el tamaño en y: ")
        if size_y.isdigit():
            size_y = int(size_y)
            break
    aux = 0
    while True:
        aux += 1
        while True:
            coor_x = input("Ingrese la coordenada x del monticulo {}: ".format(aux))
            if coor_x.isdigit():
                coor_x = int(coor_x)
                break
        while True:
            coor_y = input("Ingrese la coordenada y del monticulo {}: ".format(aux))
            if coor_y.isdigit():
                coor_y = int(coor_y)
                break
        while True:
            quantity = input("Ingrese la cantidad de arena del monticulo {}: ".format(aux))
            if quantity.isdigit():
                quantity = int(quantity)
                break
        coordinates[(coor_x,coor_y)] = quantity
        more = input("Desea ingresar otro monticulo? (S/N): ")
        if not more.upper() == "S":
            break
    config = input("Desea personalizar los parametros? (S/N): ")
    vertical = 1
    horizontal = 1
    vertical_mirror = 1
    horizontal_mirror = 1
    colours = ["0 0 0","255 0 255","255 0 0","255 255 0"] # Default colours
    if config.upper() == "S":
        while True:
            vertical = input("Tamaño de celda vertical: ")
            if vertical.isdigit():
                vertical = int(vertical)
                break
        while True:
            horizontal = input("Tamaño de celda horizontal: ")
            if horizontal.isdigit():
                horizontal = int(horizontal)
                break
        while True:
            vertical_mirror = input("Espejado vertical: ")
            if vertical_mirror.isdigit():
                vertical_mirror = int(vertical_mirror)
                break
        while True:
            horizontal_mirror = input("Espejado horizontal: ")
            if horizontal_mirror.isdigit():
                horizontal_mirror = int(horizontal_mirror)
                break
        conf_colour = input("Desea personalizar los colores? (S/N): ")
        if conf_colour.upper() == "S":
            colours = []
            print("Colores disponibles:")
            print(colour_list.keys())
            for n in (0,1,2,3):
                while True:
                    selected = input("Escriba el color que representa el {}:".format(n))
                    if selected.upper() in colour_list:
                        colours.append(colour_list[selected.upper()])
                        break
                    print("Por favor, escriba un color de la lista")
    # Generate the map
    print("Procesando, espere por favor...")
    while True:
        coordinates,repeat = topple(coordinates,size_x,size_y)
        if not repeat:
            break
    # Generate the content of the file
    head = generate_head(size_x,size_y,horizontal,vertical,horizontal_mirror,vertical_mirror)
    body_list = generate_body(coordinates,colours,size_x,size_y)
    body = mirror(body_list,horizontal_mirror,vertical_mirror)
    file_content = generate_text(head,body,horizontal,vertical)
    # Write into the file
    write(final_name,file_content)
    print("Final")
    return

def topple(coordinates,size_x,size_y):
    """
    Topple a given coordinate map using sandpiles method. Also, return if the map needs to be topple again.
    Params:
        coordinates (dictionary) Contains coordinate map to topple
        size_x (int) Size of x coordinates
        size_y (int) Size of y coordinates
    Return:
        dictionary: The coordinate map after the topple
        bool: True if there is a field with more than 3 sands. False otherwise.
    """
    need_to_repeat = False
    for key in list(coordinates.keys()):
        if coordinates[key] > 3:
            value = coordinates[key] // 4
            coordinates[key] = coordinates[key] % 4 # Update current field
            # for coor in (left,right,up,down)
            for coor in ((key[0]-1,key[1]), (key[0]+1,key[1]), (key[0],key[1]-1), (key[0],key[1]+1)): 
                # Not need for coordinates outside the limits
                if coor[0] >= 0 and coor[1] >= 0 and coor[0] <= size_x and coor[1] <= size_y:
                    old = coordinates.get(coor,0)
                    coordinates[coor] = old + value # Add the new value
                    if (old + value) > 3:
                        need_to_repeat = True
    return coordinates,need_to_repeat

def generate_body(coordinates,colours,size_x,size_y):
    """
    Generate the body to add in a ppm file. Every list represent a horizontal line, wich includes a list with every bit on it.
    Params:
        coordinates (dictionary) Contains coordinate map to transform
        colours (list) Must contain four colours, correspond to 0,1,2,3 respectively
        size_x (int) Size of x coordinates
        size_y (int) Size of y coordinates
    Return:
        list: List of lists of the body
    """
    y_list = []
    if not len(colours) == 4:
        return False
    for y in range(0,size_y):
        x_list = []
        for x in range(0,size_x):
            x_list.append("\n"+str(colours[coordinates.get((x,y),0)]))
        y_list.append(x_list)
    return y_list

def generate_head(size_x,size_y,horizontal,vertical,h_mirror,v_mirror):
    """
    Generate the head text to add in a ppm file.
    Params:
        size_x (int) Size of x coordinates
        size_y (int) Size of y coordinates
        horizontal (int) Pixels for each x coordinate
        vertical (int) Pixels for each y coordinate
        h_mirror (int) Times to mirror in horizontal
        v_mirror (int) Times to mirror in vertical
    Return:
        string: Text of the head
    """
    return "P3\n"+str(size_x*horizontal*h_mirror)+" "+str(size_y*vertical*v_mirror)+"\n255"

def generate_text(head,body_list,horizontal,vertical):
    """
    Create the final content of a ppm file.
    Params:
        head (string) Text for the header
        body_list (list) List of lists, than represent the body.
        horizontal (int) Pixels for each x coordinate
        vertical (int) Pixels for each y coordinate
    Return:
        string: Full content of the ppm file 
    """
    text = head
    for sub_list in body_list:
        for v in range(0,vertical):
            for pixel in sub_list:
                for h in range(0,horizontal):
                    text += pixel
    return text

def write(name,content):
    """ 
    Write or create a ppm file and insert the content.
    Params:
        name (string) Name of the file (without extension)
        content (string) Content to write in the file
    """
    final_name = name + ".ppm"
    with open(final_name,"w") as f:
        f.write(content)
    return

def mirror(body,horizontal,vertical):
    """
    Mirror the image in horizontal and vertical form
    Params:
        body (list) List of lists, than represent the body.
        horizontal (int) Times to mirror in horizontal
        vertical (int) Times to mirror in vertical
    """
    for i in range(1,horizontal): # Times to mirror in horizontal
        mirrors = []
        for y in body: # Reed every "line" to be reversed
            aux = y[::-1] # as reverse()
            mirrors.append(aux)
        for e,m in enumerate(mirrors):
            body[e].extend(mirrors[e]) # Merge both lists
    mirrors = []
    for i in range(1,vertical): # Times to mirror in vertical
        aux = body[::-1] # as reverse()
        mirrors.extend(aux)
    body.extend(mirrors) # Merge both lists
    return body

main()
