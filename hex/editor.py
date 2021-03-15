import curses


class BinEditor(object):
    def __init__(self, filepath):
        self.cursor_index = 0
        self.window_y_offset = 0
        self.byte_count = 1
        self.max_byte_count = 32
        self.width = 64
        self.little_endian = False
        self.insert_mode = False
        self.filepath = filepath

    def display_byte(self, index):
        index_y = index / self.width - self.window_y_offset
        index_x = index % self.width

        offset_x = index_x / self.byte_count * (self.byte_count * 2 + 1)
        if self.little_endian:
            offset_x += (self.byte_count - index_x % self.byte_count - 1) * 2
        else:
            offset_x += index_x % self.byte_count * 2
        self.screen.addstr(int(index_y), int(offset_x + 10), '%02X' % self.data[int(index)],
                           self.data[int(index)])

    def display_bytes(self):
        offset = self.window_y_offset * self.width
        for i in range(int(offset), int(min(len(self.data), offset + (self.max_y - 1) * self.width))):
            self.display_byte(i)

    def display_addresses(self):
        for i in range(int(self.window_y_offset),
                       int(min(len(self.data) / self.width + 1, self.window_y_offset + self.max_y - 1))):
            if (i * self.width) % 0x100 == 0:
                self.screen.addstr(int(i - self.window_y_offset), 0, '%08X:' % (i * self.width), curses.color_pair(4))
            else:
                self.screen.addstr(int(i - self.window_y_offset), 0, '%08X:' % (i * self.width))

    def display_cursor(self):
        cursor_y = self.cursor_index / 2 / self.width
        cursor_y -= self.window_y_offset
        cursor_x = self.cursor_index / 2 % self.width
        cursor_x = cursor_x * 2 + cursor_x / self.byte_count
        cursor_offset = self.cursor_index % 2
        self.screen.addstr(int(cursor_y), int(cursor_x + cursor_offset + 10), '')

    def rep_text_byte(self, c):
        if 0x20 <= c < 0x7e:
            return chr(c)
        else:
            return '.'

    def display_text_line(self, index):
        index_y = index / self.width - self.window_y_offset
        offset_x = self.width * 2 + self.width / self.byte_count + 10

        text = ''.join(
            [self.rep_text_byte(self.data[i]) for i in range(int(index), min(index + self.width, len(self.data)))])
        self.screen.addstr(int(index_y), int(offset_x), text)

    def display_text(self):
        offset = self.window_y_offset * self.width
        for i in range(int(offset), int(min(len(self.data), offset + (self.max_y - 1) * self.width)), self.width):
            self.display_text_line(i)

    def edit_byte(self, index, mode):
        if mode == "del":
            data_index = index / 2 / self.byte_count * self.byte_count
            data_index -= self.byte_count
            if data_index >= 0:
                for i in range(0, self.byte_count):
                    del self.data[int(data_index)]
        elif mode == "ins":
            data_index = index / 2
            for i in range(0, self.byte_count):
                self.data.insert(int(data_index), 0)

    def edit_byte_piece(self, index, key):
        shift = (1 - index % 2) * 4
        data_index = index / 2
        if self.little_endian:
            offset = self.byte_count - data_index % self.byte_count - 1
            data_index = offset + data_index / self.byte_count * self.byte_count
        self.data[int(data_index)] = (int(key, 16) << shift) | (
                    self.data[int(data_index)] ^ (self.data[int(data_index)] & (0xf << shift)))

    def print_info(self, msg):
        self.screen.addstr(self.max_y - 1, 1, ' ' * 40)
        self.screen.addstr(self.max_y - 1, 1, msg)

    def calculate_display_width(self):
        return self.width * 2 + self.width / self.byte_count + 10 + self.width

    def adjust_width_to_screen(self):
        while self.calculate_display_width() > self.max_x:
            self.width -= 4

    def redraw(self):
        self.screen.clear()
        self.display_addresses()
        self.display_bytes()
        self.display_text()

    def store(self, filepath):
        write_data(filepath, self.data)

    def load(self, filepath):
        self.data = read_data(filepath)

    def main(self, screen):
        self.screen = screen
        self.max_y, self.max_x = self.screen.getmaxyx()

        self.adjust_width_to_screen()

        self.screen.clear()

        self.load(self.filepath)
        self.print_info('read file: ' + self.filepath)

        self.redraw()
        self.display_cursor()

        self.screen.refresh()
        k = self.screen.getkey()
        while k != 'Q':
            if k == 'KEY_LEFT':
                self.cursor_index -= 1
                self.print_info('offset %X/%X' % (int(self.cursor_index / 2), len(self.data)))
            elif k == 'KEY_RIGHT':
                self.cursor_index += 1
                self.print_info('offset %X/%X' % (int(self.cursor_index / 2), len(self.data)))
            elif k == 'KEY_UP':
                self.cursor_index -= self.width * 2
                self.print_info('offset %X/%X' % (int(self.cursor_index / 2), len(self.data)))
            elif k == 'KEY_DOWN':
                self.cursor_index += self.width * 2
                self.print_info('offset %X/%X' % (int(self.cursor_index / 2), len(self.data)))
            elif k == 'KEY_PPAGE':
                self.cursor_index -= (self.max_y - 1) * self.width * 2
                if self.cursor_index < 0:
                    self.window_y_offset = 0
                else:
                    self.window_y_offset -= self.max_y - 1
                self.redraw()
                self.print_info('offset %X/%X' % (int(self.cursor_index / 2), len(self.data)))
            elif k == 'KEY_NPAGE':
                self.cursor_index += (self.max_y - 1) * self.width * 2
                self.window_y_offset += self.max_y - 1
                self.redraw()
                self.print_info('offset %X/%X' % (int(self.cursor_index / 2), len(self.data)))
            elif k == ']':
                if self.byte_count > 1:
                    self.byte_count /= 2
                    self.adjust_width_to_screen()
                    self.redraw()
                self.print_info('byte_count = %d' % self.byte_count)
            elif k == '[':
                if self.byte_count < self.max_byte_count:
                    self.byte_count *= 2
                    self.redraw()
                self.print_info('byte_count = %d' % self.byte_count)
            elif k == '{':
                if self.width > 4:
                    self.width -= 4
                    self.redraw()
                self.print_info('width = %d' % self.width)
            elif k == '}':
                self.width += 4
                self.adjust_width_to_screen()
                self.redraw()
                self.print_info('width = %d' % self.width)
            elif k == 'p':
                self.little_endian = not self.little_endian
                self.redraw()
                self.print_info('little_endian = {}'.format(self.little_endian))
            elif k == 'i':
                self.insert_mode = not self.insert_mode
                self.print_info('insert_mode = {}'.format(self.insert_mode))

            elif k == 'KEY_DC':
                if self.insert_mode:
                    self.edit_byte(self.cursor_index, "del")
                    self.redraw()
                    self.cursor_index -= self.byte_count * 2
                else:
                    self.print_info('not in insert mode!')

            elif len(k) == 1 and (('0' <= k <= '9') or ('a' <= k <= 'f')):
                if self.insert_mode and self.cursor_index % (self.byte_count * 2) == 0:
                    self.edit_byte(self.cursor_index, "ins")
                    self.redraw()
                self.edit_byte_piece(self.cursor_index, k)
                byte_index = self.cursor_index / 2
                if self.little_endian:
                    offset = self.byte_count - byte_index % self.byte_count - 1
                    byte_index = byte_index / self.byte_count * self.byte_count + offset
                self.display_byte(byte_index)
                self.display_text_line(byte_index / self.width * self.width)
                self.cursor_index += 1

            elif k == 'W':
                self.store(self.filepath)
                self.print_info('wrote file: ' + self.filepath)
            else:
                self.print_info('unknown command "{}"'.format(k))

            if self.cursor_index < 0:
                self.cursor_index = 0
                self.print_info('offset %X/%X' % (int(self.cursor_index / 2), len(self.data)))
            if self.cursor_index > len(self.data) * 2:
                self.cursor_index = len(self.data) * 2
                self.print_info('offset %X/%X' % (int(self.cursor_index / 2), len(self.data)))

            cursor_y = self.cursor_index / 2 / self.width
            if cursor_y - self.window_y_offset < 0:
                self.window_y_offset += cursor_y - self.window_y_offset
                self.redraw()
                self.print_info('offset %X/%X' % (int(self.cursor_index / 2), len(self.data)))
            if cursor_y - self.window_y_offset >= self.max_y - 1:
                self.window_y_offset += cursor_y - self.window_y_offset - (self.max_y - 2)
                self.redraw()
                self.print_info('offset %X/%X' % (self.cursor_index / 2, len(self.data)))

            self.display_cursor()

            self.screen.refresh()
            k = self.screen.getkey()


def read_file(filepath):
    with open(filepath, 'rb') as f:
        text = bytes(f.read())
    return text


def write_file(filepath, text):
    with open(filepath, 'wb') as f:
        f.write(text)


def read_data(filepath):
    text = read_file(filepath)

    data = [ord(chr(c)) for c in text]
    return data


def write_data(filepath, data):
    write_file(filepath, ''.join([chr(c) for c in data]))


def join_bytes(data, byte_count, little_endian=True):
    while len(data) < byte_count:
        data.append(0)
    if little_endian:
        return sum([data[i] << 8 * i for i in range(0, byte_count)])
    else:
        result = 0
        for i in range(0, byte_count):
            result = (result << 8) | data[i]
        return result


def split_bytes(data, byte_count, little_endian=True):
    if little_endian:
        return [(data >> i * 8) & 0xff for i in range(0, byte_count)]
    else:
        return [(data >> i * 8) & 0xff for i in range(byte_count - 1, -1, -1)]


def rep_data(data, byte_count):
    return ('%0' + str(byte_count * 2) + 'X') % data

