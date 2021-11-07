class PointerHouse:
    def __init__(self, point_from, point_to, value):
        """
        point_from: The house (typically column 1, 5, or 9) whose value acts as pointers
        point_to: The houses (typically the rows) that the pointers index into
        vale: The value (typically 1, 5, or 9) to place in the indexed cell
        """
        self.point_from = point_from
        self.point_to = point_to
        self.value = value
    
    def iter_pointers(self):
        """
        Iterate over the pointers in this house, as well asa the house the each respective pointer indexes into.
        """
        return zip(self.point_from, self.point_to)