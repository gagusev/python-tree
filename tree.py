from os import listdir, path, readlink
from argparse import ArgumentParser

PFX_W=2
SYM_L='└'
SYM_T='├'
SYM_V='─'
SYM_H='─'
BOLD = '\033[1m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
ENDC = '\033[0m'

class Entry:
    def __init__(self, _name, _type, _path, _target):
        self.name = _name
        self.type = _type
        self.path = _path
        self.target = _target

    def __str__(self):
        return self.name
    
    def __eq__(self, another):
        return hasattr(another, 'path') and self.path == another.path
    
    def __hash__(self):
        return hash(self.path)

def generate_tree(start_entry, depth):
    entries = {start_entry: []}
    if depth == 0:
        return entries
    for entry in listdir(start_entry.path):
        full_path = path.join(start_entry.path, entry)
        entry_target = None
        if path.isdir(full_path):
            entry_type = 'dir'
        elif path.islink(full_path):
            entry_type = 'link'
            entry_target = readlink(full_path)
        else:
            entry_type = 'file'
        entry_obj = Entry(entry, entry_type, full_path, entry_target)
        entries[start_entry].append(entry_obj)
        if entry_type == "dir":
            entries.update(generate_tree(entry_obj, depth-1))
    return entries

def print_tree(start, parent, tree, prefix=''):
    if parent != start:
        if parent.type == 'dir':
            print(f' {BOLD}{OKBLUE}{parent.name}{ENDC}')
        elif parent.type == 'link':
            print(f' {BOLD}{OKCYAN}{parent.name}{ENDC} -> {BOLD}{OKGREEN}{parent.target}{ENDC}')
        else:
            print(f' {parent.name}')
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

def main():
    parser = ArgumentParser(description="displays the directory structure as a tree with a specified depth")

    parser.add_argument('-L', '--depth',
                        type=int,
                        default=100,
                        help='Depth (nesting level) to display')
    
    parser.add_argument('dir',
                        type=str,
                        help="Path to the directory")

    args = parser.parse_args()

    init_entry = Entry(args.dir, 'dir', path.abspath(args.dir), None)
    print(f'{BOLD}{OKBLUE}{init_entry.name}{ENDC}')
    print_tree(init_entry, init_entry, generate_tree(init_entry, args.depth))

if __name__ == '__main__':
    main()