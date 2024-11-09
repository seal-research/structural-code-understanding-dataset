import java.io.*;
import java.util.*;

public class MazeSolver
{
    private static String[] readLines (InputStream f) throws IOException
    {
        BufferedReader r =
            new BufferedReader (new InputStreamReader (f, "US-ASCII"));
        ArrayList<String> lines = new ArrayList<String>();
        String line;
        while ((line = r.readLine()) != null)
            lines.add (line);
        return lines.toArray(new String[0]);
    }

    private static char[][] decimateHorizontally (String[] lines)
    {
        final int width = (lines[0].length() + 1) / 2;
        char[][] c = new char[lines.length][width];
        for (int i = 0  ;  i < lines.length  ;  i++)
            for (int j = 0  ;  j < width  ;  j++)
                c[i][j] = lines[i].charAt (j * 2);
        return c;
    }

    private static boolean solveMazeRecursively (char[][] maze,
                                                 int x, int y, int d)
    {
        boolean ok = false;
        for (int i = 0  ;  i < 4  &&  !ok  ;  i++)
            if (i != d)
                switch (i)
                    {
                    case 0:
                        if (maze[y-1][x] == ' ')
                            ok = solveMazeRecursively (maze, x, y - 2, 2);
                        break;
                    case 1:
                        if (maze[y][x+1] == ' ')
                            ok = solveMazeRecursively (maze, x + 2, y, 3);
                        break;
                    case 2:
                        if (maze[y+1][x] == ' ')
                            ok = solveMazeRecursively (maze, x, y + 2, 0);
                        break;
                    case 3:
                        if (maze[y][x-1] == ' ')
                            ok =