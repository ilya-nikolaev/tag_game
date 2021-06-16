from typing import Any


class Matrix:
    def __init__(self, body: list[list[Any]]):
        
        self._body = body
        self._validate_body()
        
        self._height = len(self._body)
        self._width = len(self._body[0])
    
    @classmethod
    def from_size(cls, width: int, height: int):
        
        cls._validate_size(width, height)
        
        return cls([
            [0 for _ in range(width)]
            for _ in range(height)
        ])
    
    def _validate_body(self):

        length = None
        for row in self._body:
            if length is None:
                length = len(row)
            elif len(row) != length:
                raise ValueError("lengths of the lists inside don`t match")
    
    @staticmethod
    def _validate_size(width: int, height: int):
        
        size = (width, height)
        
        if not all(isinstance(num, int) for num in size):
            raise ValueError("dimensions are must be integers")
        if not all(num >= 1 for num in size):
            raise ValueError("dimensions are must be bigger than 1")
    
    def index(self, value):
        # TODO: optimize
        for i, row in enumerate(self._body):
            if value in row:
                return row.index(value), i
        
        raise ValueError(f"{repr(value)} is not in matrix")
    
    def max(self):
        return max([max(row) for row in self._body])
    
    def min(self):
        return min([min(row) for row in self._body])
    
    def _max_str_len(self):
        max_len = max(
            [max(row, key=lambda x: len(str(x))) for row in self._body],
            key=lambda x: len(str(x))
        )
        
        return len(str(max_len))
        
    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._body)})'
    
    def __str__(self):
        total = list()
        
        max_len = self._max_str_len() + 1
        for row in self._body:
            total.append(' '.join(f"{el:<{max_len}}" for el in row))
        
        return '\n' + '\n'.join(total) + '\n'

    def __getitem__(self, item: tuple[int, int]):
        x, y = item
    
        if x > self._width - 1 or y > self._height - 1:
            raise IndexError('matrix index out of range')
    
        return self._body[y][x]
    
    def __setitem__(self, key: tuple[int, int], value):
        x, y = key
        self._body[y][x] = value
