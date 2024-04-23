from os import listdir, path

PFX_W=2
SYM_L='└'
SYM_T='├'
SYM_V='─'
SYM_H='─'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
ENDC = '\033[0m'

class Entry:
    def __init__(self, _name, _type, _path):
        self.name = _name
        self.type = _type
        self.path = _path

    def __str__(self):
        return self.name
    
    def __eq__(self, another):
        return hasattr(another, 'path') and self.path == another.path
    
    def __hash__(self):
        return hash(self.path)

def generate_tree(start_entry):
    entries = {start_entry: []}
    for entry in listdir(start_entry.path):
        full_path = path.join(start_entry.path, entry)
        if path.isdir(full_path):
            entry_type = 'dir'
        elif path.islink(full_path):
            entry_type = 'link'
        else:
            entry_type = 'file'
        entry_obj = Entry(entry, entry_type, full_path)
        entries[start_entry].append(entry_obj)
        if entry_type == "dir":
            entries.update(generate_tree(entry_obj))
    return entries

def print_tree(start, parent, tree, prefix=''):
    if parent != start:
        if parent.type == 'dir':
            print(f' {OKBLUE}{parent}{ENDC}')
        elif parent.type == 'link':
            print(f' {OKCYAN}{parent}{ENDC}')
        else:
            print(f' {parent}')
    if parent not in tree:
        return
    for child in tree[parent][:-1]:
        print(prefix + SYM_T + SYM_V * PFX_W, end='')
        print_tree(start, child, tree, prefix + '│' + ' ' * PFX_W + ' ')
    if not tree[parent]:
        return
    child = tree[parent][-1]
    print(prefix + SYM_L + SYM_H * PFX_W, end='')
    print_tree(start, child, tree, prefix + ' ' * (PFX_W + 1) + ' ')

# dct = {
#     Entry('/', 'dir', '/'): [Entry('usr', 'dir', '/usr/'),
#                              Entry('bin', 'dir', '/bin/'),
#                              Entry('etc', 'dir', '/etc/')],
#     Entry('usr', 'dir', '/usr/'): [Entry('local', 'dir', '/usr/local/'),
#                                    Entry('readme.md', 'file', '/usr/readme.md')],
#     Entry('local', 'dir', '/usr/local/'): [Entry('bin', 'dir', '/usr/local/bin/')]       
# }

#print(Entry('/', 'dir', '/'))
#print_tree(Entry('/', 'dir', '/'), Entry('/', 'dir', '/'), dct)

start = Entry('python_tree', 'dir', '/home/grigus/python_tree/')
directory_dict = generate_tree(start)
print('../braim-task2')
print_tree(start, start, directory_dict)