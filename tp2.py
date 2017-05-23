def main():
    """
    Primary function of the program.
    """
    coordinates = {}
    # User input
    colour_list= {"BLANCO":"255 255 255","NEGRO":"0 0 0","MAGENTA":"255 0 255","AMARILLO":"255 255 0","ROJO":"255 0 0","VERDE":"0 255 0","AZUL": "0 0 255"}
    final_name = input("Ingrese del nombre del archivo sin extencion: ")
    size_x = ask_number("Ingrese el tamaño en x: ")
    size_y = ask_number("Ingrese el tamaño en y: ")
    aux = 0
    while True:
        aux += 1
        coor_x = ask_number("Ingrese la coordenada x del monticulo {}: ",aux)
        coor_y = ask_number("Ingrese la coordenada y del monticulo {}: ",aux)
        quantity = ask_number("Ingrese la cantidad de arena del monticulo {}: ",aux)
        coordinates[(coor_x,coor_y)] = quantity
        more = input("Desea ingresar otro monticulo? (SI/NO): ")
        if not more.upper() == "SI":
            break
    config = input("Desea personalizar los parametros? (SI/NO): ")
    vertical = 1
    horizontal = 1
    vertical_mirror = 1
    horizontal_mirror = 1
    colours = ["0 0 0","255 0 255","255 0 0","255 255 0"] # Default colours
    if config.upper() == "SI":
        vertical = ask_number("Tamaño de celda vertical: ")
        horizontal = ask_number("Tamaño de celda horizontal: ")
        vertical_mirror = ask_number("Espejado vertical: ")
        horizontal_mirror = ask_number("Espejado horizontal: ")
        conf_colour = input("Desea personalizar los colores? (SI/NO): ")
        if conf_colour.upper() == "SI":
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
    # Set list of parameters
    size = [size_x,size_y]
    pixel_size = [horizontal,vertical]
    mirror = [horizontal_mirror,vertical_mirror]
    # Generate the map
    print("Procesando, espere por favor...")
    coordinates = generate_map(coordinates,size)
    # Generate the content of the file
    head = generate_head(size,pixel_size,mirror)
    body_list = generate_body(coordinates,colours,size)
    body = mirror(body_list,mirror)
    file_content = generate_text(head,body,pixel_size)
    # Write into the file
    write_file(final_name,file_content)
    print("Final")
    return

def generate_map(coordinates,size):
    """
    
    """
    while True:
        coordinates,repeat = topple(coordinates,size)
        if not repeat:
            break
    return coordinates

def topple(coordinates,size):
    """
    Topple a given coordinate map using sandpiles method. Also, return if the map needs to be topple again.
    Params:
        coordinates (dictionary) Contains coordinate map to topple
        size (list) Contains x and y coordinates, in that order
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
                if coor[0] >= 0 and coor[1] >= 0 and coor[0] <= size[0] and coor[1] <= size[1]:
                    old = coordinates.get(coor,0)
                    coordinates[coor] = old + value # Add the new value
                    if (old + value) > 3:
                        need_to_repeat = True
    return coordinates,need_to_repeat

def generate_body(coordinates,colours,size):
    """
    Generate the body to add in a ppm file. Every list represent a horizontal line, wich includes a list with every bit on it.
    Params:
        coordinates (dictionary) Contains coordinate map to transform
        colours (list) Must contain four colours, correspond to 0,1,2,3 respectively
        size (list) Contains x and y coordinates, in that order
    Return:
        list: List of lists of the body
    """
    y_list = []
    if not len(colours) == 4:
        return False
    for y in range(0,size[1]):
        x_list = []
        for x in range(0,size[0]):
            x_list.append("\n"+str(colours[coordinates.get((x,y),0)]))
        y_list.append(x_list)
    return y_list

def generate_head(size,pixel_size,mirror):
    """
    Generate the head text to add in a ppm file.
    Params:
        size (list) Contains x and y coordinates, in that order
        pixel_size (list) Contains pixels quantity for each x and y coordinate, in that order
        mirror (list) Contains times to mirror in horizontal and vertical, in that order
    Return:
        string: Text of the head
    """
    return "P3\n"+str(size[0]*pixel_size[0]*mirror[0])+" "+str(size[1]*pixel_size[1]*mirror[1])+"\n255"

def generate_text(head,body_list,pixel_size):
    """
    Create the final content of a ppm file.
    Params:
        head (string) Text for the header
        body_list (list) List of lists, than represent the body.
        pixel_size (list) Contains pixels quantity for each x and y coordinate, in that order
    Return:
        string: Full content of the ppm file 
    """
    text = head
    for sub_list in body_list:
        for v in range(0,pixel_size[1]):
            for pixel in sub_list:
                for h in range(0,pixel_size[0]):
                    text += pixel
    return text

def write_file(name,content):
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

def mirror(body,mirror):
    """
    Mirror the image in horizontal and vertical form
    Params:
        body (list) List of lists, than represent the body.
        mirror (list) Contains times to mirror in horizontal and vertical, in that order
    """
    for i in range(1,mirror[0]): # Times to mirror in horizontal
        mirrors_aux = []
        for y in body: # Reed every "line" to be reversed
            aux = y[::-1] # as reverse()
            mirrors_aux.append(aux)
        for e,m in enumerate(mirrors_aux):
            body[e].extend(mirrors_aux[e]) # Merge both lists
    mirrors_aux = []
    for i in range(1,mirror[1]): # Times to mirror in vertical
        aux = body[::-1] # as reverse()
        mirrors_aux.extend(aux)
    body.extend(mirrors_aux) # Merge both lists
    return body

def ask_number(message,data=None):
    """ 
    Ask for a user input and validate it to be a positive number.
    Params:
        message (string) Input content
        data (optional) String or number to be show in the input by format method.
    Return:
        int: Int value of user input
    """
    while True:
        ask = input(message.format(data))
        if ask.isdigit() and ask > 0:
            ask = int(ask)
            break
        print("Debe ingresar un numero positivo.")
    return ask

main()
