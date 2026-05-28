def check_term_size(self) -> bool:
    """This function checks if the terminal is big enough
    to display the maze with the display function.

    The function returns a bool.
    """
    columns, lines = os.get_terminal_size()
    if columns < (self.width + 1) * 6 or lines < self.height * 2:
        os.system('clear')
        print("Terminal size too small")
        return False

    return True
