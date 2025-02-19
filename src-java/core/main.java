package core;

import AI.BFS;
import model.Board;
import model.Cell;
import model.Node;

import java.util.Hashtable;
import java.util.Scanner;

public class main {

    public static void main(String[] args) {
        System.out.println(" pls enter rows and columns of your board : \n");
        Scanner sc = new Scanner(System.in);
        String mn = sc.nextLine();
        int rows = Integer.parseInt(mn.split(" ")[0]);
        int columns = Integer.parseInt(mn.split(" ")[1]);
        String[][] board = new String[rows][columns];
        String[] lines = new String[rows];
        for (int i = 0; i < rows; i++) {
            lines[i] = sc.nextLine();
            String[] line = lines[i].split(" ");
            if (columns >= 0) System.arraycopy(line, 0, board[i], 0, columns);
        }
        Mapper mapper = new Mapper();
        Cell[][] cells = mapper.createCells(board, rows, columns);
        Board gameBoard = mapper.createBoard(cells, rows, columns);
        Hashtable<String, Boolean> initHash = new Hashtable<>();
        initHash.put(Cell.getStart().toString(), true);
        Node start = new Node(Cell.getStart(), Cell.getStart().getValue(), Cell.getGoal().getValue(), gameBoard, null, initHash);
        BFS bfs = new BFS();
        bfs.search(start);
    }
}
