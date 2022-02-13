from ast import literal_eval
from PIL import Image, ImageDraw
import os
import sys

### Sort Dictionary Reverse Numerically ###
def sorted_dict(dictionary):
    output_dict = dict()
    dict_keys = sorted(dictionary.keys())
    for i in dict_keys:
        output_dict[i] = dictionary[i]
    return output_dict

### Compress Dictionary Leaving No Gaps in Numbers ###
def compressed_dict(dictionary):
    keys = list(dictionary.keys())
    for key in keys:
        while key-1 not in list(dictionary.keys()) and key > 1: dictionary[key-1] = dictionary[key]; del dictionary[key]; key = key-1
    return dictionary

### Reverse Dictionary ###
def reversed_dict(dictionary):
    output_dict = dict()
    dict_keys = list(dictionary.keys())
    dict_keys.reverse()
    for i in dict_keys:
        output_dict[i] = dictionary[i]
    return output_dict

### Set Order of Current Layer ###
def set_order(layer, dictionary):
    try: z_index = int(input(f"What index position would you like {layer} to be placed (1 = first layer, usually background): "))
    except ValueError: print("Index value must be integer."); return set_order(layer, dictionary)
    except: print("Unexpected Error... restarting."); main()
    if z_index in list(dictionary.keys()): print("Index value is already taken."); return set_order(layer, dictionary)
    elif z_index < 1: print("Index value must be positive."); return set_order(layer, dictionary)
    else: return int(z_index)

### Set Resolution of Images ###
def set_res():
    try: width = input("Enter Image Width in Pixels: ")
    except ValueError: print("Resolution must be integer."); return set_res()
    except: print("Unexpected Error!"); return set_res()
    try: height = input("Enter Image Height in Pixels: ")
    except ValueError: print("Resolution must be integer."); return set_res()
    except: print("Unexpected Error!"); return set_res()
    if height < 1 or width < 1: print("Resolution must be positive."); return set_res()
    return (width, height)

### Confirm Layer Ordering ###
def order_confirmation():
    restart = input("Is this order correct? y | n: ")
    if restart.lower().startswith('n'): return False
    elif restart.lower().startswith('y'): return True
    else: print("Invalid option. Choose y or n."); return order_confirmation()

def main():
    ### Initialize Variables ###
    assets = os.listdir("./assets")
    order = dict()
    layer_dict = dict()

    ### Get Layers ###
    layers = [asset for asset in assets if os.path.isdir("./assets/" + asset)]

    layer_count = len(layers)

    ### Layer Rules ###
    if layer_count > 15:
        sys.exit("You can have at most 15 layers.")
    elif layer_count <= 1:
        sys.exit("Must have at least 2 layers.")

    ### Set Resolution ###
    resolution = set_res()

    ### Set Layer Order ###
    for layer in layers:
        z_index = set_order(layer, order)
        order[z_index] = layer

    ### Sort Order ###
    order = sorted_dict(order)
    order = compressed_dict(order)
    order = reversed_dict(order)

    ### Confirm Order ###
    for i in list(order.keys()):
        print(f"{i}: {order[i]}")
    if not order_confirmation(): main()

    ### Get Dict for All Layer Items ###
    for layer in list(order.values()):
        layer_dict[layer] = [Image.open("./assets/"+layer+"/"+file).convert(mode='RGBA').resize(resolution, resample=Image.NEAREST) for file in os.listdir("./assets/"+layer) if file.endswith(".png")]

    ### Combine Layers ###
    count = 0
    for l1 in layer_dict[order[1]]:
        for l2 in layer_dict[order[2]]:
            last = Image.alpha_composite(l1, l2)
            if layer_count > 2:
                for l3 in layer_dict[order[3]]: 
                    last = Image.alpha_composite(last, l3)
                    if layer_count > 3:
                        for l4 in layer_dict[order[4]]:
                            last = Image.alpha_composite(last, l4)
                            if layer_count > 4:
                                for l5 in layer_dict[order[5]]:
                                    last = Image.alpha_composite(last, l5)
                                    count += 1; last.save("./output/"+str(count)+".png")
                            else: count += 1; last.save("./output/"+str(count)+".png")
                    else: count += 1; last.save("./output/"+str(count)+".png")
            else: count += 1; last.save("./output/"+str(count)+".png")

if __name__ == "__main__":
    main()