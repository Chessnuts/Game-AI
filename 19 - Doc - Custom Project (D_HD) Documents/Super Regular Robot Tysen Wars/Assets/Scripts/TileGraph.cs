using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

[System.Serializable]
public class TileGraph : MonoBehaviour
{
    public Unit selectedUnit = null;

    public TileGraphNode[] nodeType;

    public int[,] nodes;

    public Node[,] graph;

    int mapSizeX = 18;
    int mapSizeY = 11;

    public Text winText;
    /*
    public int playerScore;
    public int enemyScore;
    */

    public GameObject redHighlight;
    public GameObject blueHighlight;

    public List<Node> highlightedTiles;
    public List<Node> highlightedRange;
    List<Node> currentPath = new List<Node>();

    public bool isPlayerTurn = true;

    public List<Unit> playerUnits;
    public List<Unit> EnemyUnits;

    void Start()
    {
        //Initialise graph + Tiles
        InitializeMapGraph();
        //playerScore = 0;
        //enemyScore = 0;
    }



    void Update()
    {
        if (isPlayerTurn == true)
        {
            if (Input.GetKeyDown(KeyCode.Return))
            {
                DeactivateHighlights();
                ChangeTurn();
            }
        }
    }

public void runEnemyPhase()
    {
        //enemy Ai
        foreach (Unit u in EnemyUnits)
        {
            selectedUnit = u;
            Unit target = null;
            //if a player is already in range from pos attack player
            List<Node> r = GenerateRange
                    (
                    (int)(u.transform.position.x - 0.5f),
                    (int)(u.transform.position.y - 0.5f),
                    u.range,
                    false
                    );
            foreach (Node n in r)
            {
                foreach (Unit p in playerUnits)
                {
                    if (n.x == (int)(p.transform.position.x - 0.5f) && n.y == (int)(p.transform.position.y - 0.5f))
                    {
                        target = p;
                    }
                }
            }
            if (target == null)
            {
                //Debug.Log("part2");
                Unit bt = null;
                int lowestCount = 1000;
                //else look for closest player and follow path
                foreach (Unit p in playerUnits)
                {
                    GeneratePath((int)(p.transform.position.x - 0.5f), (int)(p.transform.position.y - 0.5f));

                    if (currentPath.Count < lowestCount)
                    {
                        bt = p;
                    }
                }
               // Debug.Log(bt.mov.ToString());

                graph[(int)(bt.transform.position.x - 0.5f), (int)(bt.transform.position.y - 0.5f)].redHighlight.SetActive(true);

                GeneratePath((int)(bt.transform.position.x - 0.5f), (int)(bt.transform.position.y - 0.5f));

                selectedUnit.FollowPath();

                DeactivateHighlights();

                r = GenerateRange
                    (
                    (int)(u.transform.position.x - 0.5f),
                    (int)(u.transform.position.y - 0.5f),
                    u.range,
                    false
                    );
                //else if a player is in range after moving
                foreach (Node n in r)
                {
                    foreach (Unit p in playerUnits)
                    {
                        if (n.x == (int)(p.transform.position.x - 0.5f) && n.y == (int)(p.transform.position.y - 0.5f))
                        {
                            target = p;
                        }
                    }
                }

            }
            //if found a target, damage
            if (target != null)
            {
                graph[(int)(target.transform.position.x - 0.5f), (int)(target.transform.position.y - 0.5f)].redHighlight.SetActive(true);
                target.Damage();
                //yield return new WaitForSecondsRealtime(2);
                DeactivateHighlights();
            }
            u.hasMoved = true;
        }
        selectedUnit = null;
        ChangeTurn();
    }

    private void InitializeMapGraph()
    {
        nodes = new int[mapSizeX, mapSizeY];


        //Initialise map tiles as default type
        for (int x = 0; x < mapSizeX; x++)
        {
            for (int y = 0; y < mapSizeY; y++)
            {
                nodes[x, y] = 0;
            }
        }
        //Hard code for testing

        //bottom 2 rows unwalkable
        for (int x = 0; x < mapSizeX; x++)
        {
            nodes[x, 0] = 1;
            nodes[x, 1] = 1;
        }
        //Top Row Unwalkable
        for (int x = 0; x < mapSizeX; x++)
        {
            nodes[x, mapSizeY - 1] = 1;
        }

        //Left 2 columns
        for (int y = 0; y < mapSizeY; y++)
        {
            nodes[0, y] = 1;
            nodes[1, y] = 1;
        }

        //Right 2 columns
        for (int y = 0; y < mapSizeY; y++)
        {
            nodes[0, mapSizeY - 1] = 1;
            nodes[1, mapSizeY - 2] = 1;
        }

        //other individual tiles
        //leftmost obsticles
        nodes[4, 4] = 1;
        nodes[5, 4] = 1;

        nodes[4, 7] = 1;
        nodes[5, 7] = 1;

        //middle obsticles
        nodes[8, 4] = 1;
        nodes[9, 4] = 1;

        nodes[8, 7] = 1;
        nodes[9, 7] = 1;

        //rightmost obsticles
        nodes[12, 4] = 1;
        nodes[13, 4] = 1;

        nodes[12, 7] = 1;
        nodes[13, 7] = 1;

        //Read from file
        // didn't finish :/

        //graph list variable used for edges 
        graph = new Node[mapSizeX, mapSizeY];

        //Initialize array
        for (int x = 0; x < mapSizeX; x++)
        {
            for (int y = 0; y < mapSizeY; y++)
            {
                graph[x, y] = new Node();

                graph[x, y].x = x;
                graph[x, y].y = y;
            }
        }

        //add edges
        for (int x = 0; x < mapSizeX; x++)
        {
            for (int y = 0; y < mapSizeY; y++)
            {
                //If x is greater than 0, add left neighbouring space
                if (x > 0)
                {
                    graph[x, y].edges.Add(graph[x - 1, y]);
                }
                //If x is greater than 0, add left neighbouring space
                if (x < mapSizeX - 1)
                {
                    graph[x, y].edges.Add(graph[x + 1, y]);
                }
                //If x is greater than 0, add left neighbouring space
                if (y > 0)
                {
                    graph[x, y].edges.Add(graph[x, y - 1]);
                }
                //If x is greater than 0, add left neighbouring space
                if (y < mapSizeY - 1)
                {
                    graph[x, y].edges.Add(graph[x, y + 1]);
                }
            }
        }

        //Spawn Nodes
        for (int x = 0; x < mapSizeX; x++)
        {
            for (int y = 0; y < mapSizeY; y++)
            {
                TileGraphNode n = nodeType[nodes[x, y]];
                GameObject go = Instantiate
                    (
                    n.node,
                    new Vector2(((float)x + 0.5f), ((float)y + 0.5f)),
                    Quaternion.identity
                    );


                ClickableTile ct = go.GetComponent<ClickableTile>();
                ct.TileX = x;
                ct.TileY = y;
                ct.map = this;
            }
        }

        for (int x = 0; x < mapSizeX; x++)
        {
            for (int y = 0; y < mapSizeY; y++)
            {

                graph[x, y].redHighlight = Instantiate
                (
                    redHighlight,
                    new Vector2(((float)x + 0.5f), ((float)y + 0.5f)),
                    Quaternion.identity
                );

                graph[x, y].blueHighlight = Instantiate
                    (
                    blueHighlight,
                    new Vector2(((float)x + 0.5f), ((float)y + 0.5f)),
                    Quaternion.identity
                    );
                graph[x, y].redHighlight.SetActive(false);
                graph[x, y].blueHighlight.SetActive(false);
            }
        }
    }




    public bool CanTraverse(int x, int y)
    {
        /*
        if (nodeType[nodes[x, y]].isWalkable == false)
        {
            return false;
        }
        
        foreach (Unit u in EnemyUnits)
        {
            if(x == (int)(u.transform.position.x - 0.5f) && y == (int)(u.transform.position.y - 0.5f))
            {
                return false;
            }
        }
        foreach (Unit u in playerUnits)
        {
            if (x == (int)(u.transform.position.x - 0.5f) && y == (int)(u.transform.position.y - 0.5f))
            {
                return false;
            }
        }
        return true;
        */
        return nodeType[nodes[x, y]].isWalkable;
    }

    public void GeneratePath(int x, int y)
    {
        selectedUnit.GetComponent<Unit>().currentPath = null;

        Dictionary<Node, float> dist = new Dictionary<Node, float>();
        Dictionary<Node, Node> prev = new Dictionary<Node, Node>();

        //Queue set up
        List<Node> unvisited = new List<Node>();

        //Get the X and Y Co-ord from pos 
        int sourceX = (int)(selectedUnit.transform.position.x - 0.5f);
        int sourceY = (int)(selectedUnit.transform.position.y - 0.5f);
        Node source = graph[sourceX, sourceY];
        Node target = graph[x, y];

        dist[source] = 0;
        prev[source] = null;

        foreach (Node v in graph)
        {
            if (v != source)
            {
                dist[v] = Mathf.Infinity;
                prev[v] = null;
            }

            unvisited.Add(v);
        }

        while (unvisited.Count > 0)
        {
            //the closest unvisited node
            Node closestNode = null;

            foreach (Node possibleClosest in unvisited)
            {
                if (closestNode == null || dist[possibleClosest] < dist[closestNode])
                {
                    closestNode = possibleClosest;
                }
            }

            if (closestNode == target)
            {
                //target found!
                break;
            }

            //Now we have visited it, remove it
            unvisited.Remove(closestNode);

            foreach (Node n in closestNode.edges)
            {
                float d = dist[closestNode] + closestNode.DistanceTo(n);
                if (d < dist[n] && CanTraverse(n.x, n.y))
                {
                    dist[n] = d;
                    prev[n] = closestNode;
                }
            }
        }

        if (prev[target] == null)
        {
            //no route between the target and source nodes

            return;
        }

        List<Node> currentPath = new List<Node>();

        Node current = target;

        // step back through to find route from the target
        while (current != null)
        {
            currentPath.Add(current);
            current = prev[current];
        }

        //reverse path from target to source to make it a path from source to target
        currentPath.Reverse();

        selectedUnit.GetComponent<Unit>().currentPath = currentPath;

    }

    public List<Node> GenerateRange(int x, int y, int size, bool traversing)
    {
        //final list that gets sent back
        List<Node> finalList = new List<Node>();

        //tempory list of nodes that still need searching
        List<Node> workinglist = new List<Node>();

        List<Node> templist = new List<Node>();

        //add starting position to temp list
        finalList.Add(graph[x, y]);

            foreach (Node e in graph[x, y].edges)
            {
                if (CanTraverse(e.x, e.y) | traversing == false)
                    workinglist.Add(e);
            }

        for (int i = 1; i <= size;)
        {
            //clear the temp list
            templist.Clear();

            //copy workinglist over to temp list
            foreach (Node n in workinglist)
            {
                templist.Add(n);
            }

            //copy workinglist over to final list
            foreach (Node n in workinglist)
            {
                if(CanTraverse(n.x, n.y) | traversing == false)
                finalList.Add(n);
            }

            //now that there are 2 copys of working list clear it as it needs to be filled with some new nodes
            workinglist.Clear();

            //For every node in the temp list, add all of it's edges to the working list
            foreach (Node n in templist)
            {
                foreach(Node e in n.edges)
                {
                    if (CanTraverse(e.x, e.y) | traversing == false)
                    workinglist.Add(e);
                }
            }

            i++;

            if(i == size)
            {
                foreach(Node n in workinglist)
                {
                    finalList.Add(n);
                }
            }
        }
        //Debug.Log("generates list");
        return finalList;
    }

    public void ActivateSelectighlight() 
    {
        if (highlightedRange != null)
        {
            foreach (Node n in highlightedRange)
            {
                if (CanTraverse(n.x, n.y))
                {
                    //Debug.Log("activations?");
                    n.redHighlight.SetActive(true);
                }
            }
        }
        if (highlightedTiles != null)
        {
            foreach (Node n in highlightedTiles)
            {
                if (CanTraverse(n.x, n.y))
                {
                    //Debug.Log("activations?");
                    n.blueHighlight.SetActive(true);
                }
            }
        }
    }

    public void DeactivateHighlights()
    {
        foreach(Node n in graph)
        {
            n.blueHighlight.SetActive(false);
            n.redHighlight.SetActive(false);
        }
        highlightedTiles = null;
        highlightedRange = null;
    }

    public void ChangeTurn()
    {
        if(isPlayerTurn == true)
        {
            foreach(Unit u in playerUnits)
            {
                u.hasMoved = true;
            }
            foreach (Unit u in EnemyUnits)
            {
                u.hasMoved = false;
            }
        }
        else
        {
            foreach (Unit u in playerUnits)
            {
                u.hasMoved = false;
            }
            foreach (Unit u in EnemyUnits)
            {
                u.hasMoved = true;
            }
        }
        isPlayerTurn = !isPlayerTurn;

        if (isPlayerTurn == false)
        {
            runEnemyPhase();
        }
    }
}