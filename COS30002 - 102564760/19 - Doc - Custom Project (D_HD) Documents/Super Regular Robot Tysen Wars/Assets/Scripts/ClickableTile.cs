using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class ClickableTile : MonoBehaviour
{
    public int TileX;
    public int TileY;
    public TileGraph map;

    private void OnMouseDown()
    {
        Debug.Log("click");
        if ( map.selectedUnit != null )
        {
            if (map.highlightedTiles != null)
            {
                foreach (Node t in map.highlightedTiles)
                {
                    Debug.Log("ct" + t.x.ToString() + " " + t.y.ToString());
                    if (t.x == TileX && t.y == TileY)
                    {
                        map.GeneratePath(TileX, TileY);
                        map.selectedUnit.FollowPath();
                        map.DeactivateHighlights();
                        map.selectedUnit.hasMoved = true;
                        break;
                    }
                }
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

    }
}
