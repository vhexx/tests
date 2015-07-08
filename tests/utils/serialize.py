# gets question list of ImagePair id's and returns serialized string
def serialize_image_pair_ids(image_pair_ids):
    image_pair_ids_string = ''
    for p in image_pair_ids:
        image_pair_ids_string = image_pair_ids_string + str(p) + ';'
    return image_pair_ids_string[:-1]


# gets serialized string and resturns list of ids(int)
def deserialize_image_pair_ids(image_pair_ids_string):
    if len(serialize_image_pair_ids([])) == 0:
        return []
    return list(map(lambda c: int(c), image_pair_ids_string.split(';')))