class FileHandler:
    def __init__(self, filename):
        self.filename = filename
        file = open(filename, 'r')
        self.lines = file.read().splitlines()

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, item):
        line_index = item
        col_index = None
        if isinstance(item, tuple):
            line_index = item[0]
            col_index = item[1]
        if isinstance(line_index, slice):
            if col_index is not None:
                raise TypeError("can't specify column on a slice")
            return self.lines[line_index]
        elif isinstance(line_index, int):
            line = self.lines[line_index]
            if col_index is None:
                return line
            elif isinstance(col_index, int) or isinstance(col_index, slice):
                return line[col_index]
            raise TypeError("column indices must be integers")
        raise TypeError("line indices must be integers")
