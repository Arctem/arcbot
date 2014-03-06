def load_array(file_name):
    try:
        f = open(file_name, 'r')
        data = f.read().split()
        f.close()
        return data
    except:
        return []

def save_array(file_name, array):
    f = open(file_name, 'w')
    for i in array:
        f.write('{}\n'.format(i))
    f.close()
