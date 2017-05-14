import utils


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

    def error(self, message, line_index, col_index=None):
        if isinstance(line_index, tuple):
            line_index, col_index = line_index
        msg = self.filename + ', '
        if isinstance(line_index, slice):
            msg += 'lines {start} to {end}'.format(start=line_index.start+1, end=line_index.stop)
            err = '\n'.join(self.lines[line_index])
        else:
            msg += 'line {index}'.format(index=line_index+1)
            err = self.lines[line_index]
        if col_index is not None:
            msg += ', '
            if isinstance(col_index, slice):
                msg += 'columns {start} to {end}'.format(start=col_index.start+1, end=col_index.stop)
            else:
                msg += 'column {index}'.format(index=col_index+1)
        msg += '\n' + err + '\n'
        pointer = ''
        if isinstance(col_index, slice):
            pointer += ' ' * col_index.start + '^' * (col_index.stop - col_index.start)
        elif isinstance(col_index, int):
            pointer += ' ' * col_index + '^'
        if len(pointer) > 0:
            msg += pointer + ' '
        msg += message
        utils.err(msg)
