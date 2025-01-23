def any_int(x, y, z):
    return (x + y == z or x + z == y or y + z == x) and isinstance(x, int) and isinstance(y, int) and isinstance(z, int)