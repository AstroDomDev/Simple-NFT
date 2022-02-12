from PIL import Image
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

    ### Get Layers ###
    layers = [asset for asset in assets if os.path.isdir("./assets/" + asset)]

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



if __name__ == "__main__":
    main()