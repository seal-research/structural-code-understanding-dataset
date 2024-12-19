from __future__ import print_function
from shapely.geometry import LineString

def recursive_simplify(line, tolerance, depth=0, max_depth=5):
    # Base case: stop if we reach max depth or if line cannot be simplified further
    if depth >= max_depth:
        return line
    
    # Simplify the line with the given tolerance
    simplified_line = line.simplify(tolerance, preserve_topology=False)
    
    # If the simplified line is identical to the input, we stop recursing
    if simplified_line.equals(line):
        return simplified_line
    
    # Recursive case: call the function again with the simplified line
    return recursive_simplify(simplified_line, tolerance, depth + 1, max_depth)

if __name__ == "__main__":
    # Create the LineString geometry
    line = LineString([(0,0),(0,0.1),(2,0),(0,5),(4,0),(0,7),(6,0.1),(7,9),(8,9),(9,9)])
    
    # Call the recursive simplification function
    simplified_line = recursive_simplify(line, tolerance=1.0)
    
    # Print the result
    print(simplified_line)