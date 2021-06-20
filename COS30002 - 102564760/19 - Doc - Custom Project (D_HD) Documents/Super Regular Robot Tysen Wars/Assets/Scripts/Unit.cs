using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using UnityEngine.UI;


[System.Serializable]
public class Unit : MonoBehaviour
{
    public enum UnitType
    {
        Scout = 0,
        Tank = 1,
        Sniper = 2
    }

    public TileGraph map;
    public List<Node> currentPath = new List<Node>();
    public UnitType type;
    public bool isPlayerControlled;
    public int mov;
    public int range;
    public int hp;
    public bool hasMoved;
    public Text hpText;
    // Start is called before the first frame update
    void Start()
    {
        //initiate unit type
        if (type == UnitType.Tank)
        {
            mov = 1;
            range = 2;
            hp = 3;
        }
        else if (type == UnitType.Sniper)
        {
            mov = 2;
            range = 3;
            hp = 1;
        }
        else //type must be scout or you did something wrong you are now a scout
        {
            mov = 3;
            range = 1;
            hp = 2;
        }

        if (isPlayerControlled)
        {
            map.playerUnits.Add(this);
            hasMoved = false;
        }
        else
        {   
            map.EnemyUnits.Add(this);
            hasMoved = true;
        }
    }

    // Update is called once per frame
    void Update()
    {
        /*
        if(currentPath != null)
        {
            int currentNode = 0;

            while(currentNode < currentPath.Count -1)
            {
                //Vector3 start = new Vector3(((float)currentPath[currentNode].x + 0.5f), ((float)currentPath[currentNode].y + 0.5f), 10.0f);
                //Vector3 end = new Vector3(((float)currentPath[currentNode + 1].x + 0.5f), ((float)currentPath[currentNode + 1].y + 0.5f), 10.0f);

                
                //Debug.DrawLine(start, end, Color.red);

                //currentNode++;
            }
        }
        */
        hpText.text = hp.ToString();
    }

    private void OnMouseDown()
    {
        //Debug.Log("Unit Clicked");
        //Debug.Log(map.isPlayerTurn.ToString() + isPlayerControlled.ToString() + hasMoved.ToString());
        if (map.isPlayerTurn == true)
        {
            if (isPlayerControlled == true)
            {
                if (hasMoved == false && map.selectedUnit == null)
                {
                    //Debug.Log("passed in");
                    map.DeactivateHighlights();
                    map.selectedUnit = this;
                    map.highlightedTiles = map.GenerateRange
                            (
                                (int)(map.selectedUnit.transform.position.x - 0.5f),
                                (int)(map.selectedUnit.transform.position.y - 0.5f),
                                map.selectedUnit.mov,
                                true
                            );
                    map.highlightedRange = map.GenerateRange
                            (
                                (int)(map.selectedUnit.transform.position.x - 0.5f),
                                (int)(map.selectedUnit.transform.position.y - 0.5f),
                                map.selectedUnit.mov + map.selectedUnit.range,
                                true
                            );
                    map.ActivateSelectighlight();
                    //Debug.Log("gone through");
                }
                else if (hasMoved == false && map.selectedUnit == this)
                {
                    map.DeactivateHighlights();
                    map.selectedUnit.hasMoved = true;
                    map.highlightedTiles = null;
                    map.highlightedRange = map.GenerateRange
                            (
                                (int)(map.selectedUnit.transform.position.x - 0.5f),
                                (int)(map.selectedUnit.transform.position.y - 0.5f),
                                map.selectedUnit.range,
                                false
                            );
                    map.ActivateSelectighlight();
                }
            }
            else if (isPlayerControlled == false)
            {
                if (map.selectedUnit.hasMoved)
                {
                    foreach(Node n in map.highlightedRange)
                    {
                        //if positions match
                        if (this.transform.position.x == (float)n.x + 0.5f && this.transform.position.x == (float)n.x + 0.5f)
                        {
                            map.selectedUnit = null;
                            map.DeactivateHighlights();
                            this.Damage();
                            break;
                        }
                    }
                }
            }
        }
    }
    void OnMouseOver()
    {
        if (Input.GetMouseButtonDown(1))
        {
            map.selectedUnit = null;
            map.highlightedTiles = null;
            map.DeactivateHighlights();
        }
    }
    public void MoveTo(int x, int y) 
    {
        foreach (Unit u in map.EnemyUnits)
        {
            if (x == (int)(u.transform.position.x - 0.5f) && y == (int)(u.transform.position.y - 0.5f))
            {
                return;
            }
        }
        foreach (Unit u in map.playerUnits)
        {
            if (x == (int)(u.transform.position.x - 0.5f) && y == (int)(u.transform.position.y - 0.5f))
            {
                return;
            }
        }
        this.transform.position = new Vector2((float)x + 0.5f, (float)y + 0.5f);
    }

    public void FollowPath()
    {
        int remainder = mov;

        while (remainder > 0)
        {

            if (currentPath == null)
            {
                return;
            }

            remainder--;

            //move into next tile
            MoveTo(currentPath[1].x, currentPath[1].y);

            currentPath.RemoveAt(0);

            //transform.position = new Vector2((float)currentPath[0].x + 0.5f, (float)currentPath[0].x + 0.5f);

            //when on tile left
            if (currentPath.Count == 1)
            {
                currentPath = null;
            }
        }
    }

    public void Damage()
    {
        hp--;

        if (hp <= 0)
        {
            if (isPlayerControlled)
            {
                map.playerUnits.Remove(this);
                //map.enemyScore++;
            }
            else
            {
                map.EnemyUnits.Remove(this);
                //map.playerScore++;
            }
            Destroy(this.gameObject);
            Destroy(this);
        }
    }
}
