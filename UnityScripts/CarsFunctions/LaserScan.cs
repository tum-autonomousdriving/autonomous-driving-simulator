using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using TextFileEditor;

public class LaserScan : MonoBehaviour
{
    public int ID = 1;
    public GameObject[] Detectors;

    private static int DetectorsCount = 60;

    //private ArrayList distance = new ArrayList();
    private float[] distance = new float[DetectorsCount]; //array to store distance of all the objects
    private float lastDistance; //last distance value read from the sensor
    private bool isDistanceSet; //to check if the distance value has been set or not. If not then it will set it.
    private const float maxDistance = 100f; //Maximum distance limit for the object to be detected.
    private const float minDistance = 0.5f; //Minimum distance limit for the object to be detected.

    int Index;

    void AddAllToList()
    {
        for (int i = 0; i < DetectorsCount; i++)
        {
            Detectors[i] = gameObject.transform.GetChild(i).gameObject;
        }
    }

    void Init_Detectors()
    {
        if (ID == 1)
        {
            for (int i = 0; i < DetectorsCount; i++)
            {
                Detectors[i].transform.SetPositionAndRotation(
                    transform.position,
                    Quaternion.Euler(new Vector3(0, 60f / DetectorsCount * i, 0))
                );
                // Detectors[i].transform.Rotate(Vector3.up, 1f*i, Space.Self);
            }
        }
        else if (ID == 2)
        {
            for (int i = 0; i < DetectorsCount; i++)
            {
                Detectors[i].transform.SetPositionAndRotation(
                    transform.position,
                    Quaternion.Euler(new Vector3(0, 60f / DetectorsCount * i - 90f, 0))
                );
                // Detectors[i].transform.Rotate(Vector3.up, 1f*i, Space.Self);
            }
        }
        else if (ID == 3)
        {
            for (int i = 0; i < DetectorsCount; i++)
            {
                Detectors[i].transform.SetPositionAndRotation(
                    transform.position,
                    Quaternion.Euler(new Vector3(0, 60f / DetectorsCount * i + 90f, 0))
                );
                // Detectors[i].transform.Rotate(Vector3.up, 1f*i, Space.Self);
            }
        }
        transform.Rotate(Vector3.up, -30f, Space.Self);
    }

    // Start is called before the first frame update
    void Start()
    {
        AddAllToList();
        Init_Detectors();
        Index = TextReader.ReadIntFromFile("Data/Index.txt") - 1;
        //I don't know why, but here should be -1, in order to store the data in the same path.
        // TextWriter.Replace("Data/Index.txt", (Index + 1).ToString());
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        Ray ray; // Create a ray starting at the self position and facing forward.
        Vector3 m_SelfPosition; // Where the ray starts from.
        Vector3 m_TargetPosition; // Where the ray ends at.
        Vector3 m_ForwardDirection; // the forward diriction of this object

        string OutputMessage = "# "; // Used to store the output message.

        for (int i = 0; i < DetectorsCount; i++)
        {
            m_SelfPosition = Detectors[i].transform.position;
            //TODO: Implenmentate the right way to conpute the pose of the object.
            // The ray is created from the self position and facing forward.
            m_ForwardDirection = Detectors[i].transform.forward; // The forward direction of this object.
            ray = new Ray(m_SelfPosition, m_ForwardDirection);
            //Debug.Log("Direction: " + m_ForwardDirection);
            RaycastHit hit; // Used to store the hit information.
            bool hitWorld = Physics.Raycast(ray, out hit, Mathf.Infinity);
            // Check if raycast hits any world-space geometry.

            if (hitWorld)
            { // If it did, get the hit position.
                m_TargetPosition = hit.point; // Set the target position to the hit position.
                Debug.DrawLine(m_SelfPosition, m_TargetPosition, Color.blue); // Draw a line from the self position to the hit position.
                //distance.Add(Vector3.Distance(m_SelfPosition, m_TargetPosition)); // Calculate the distance.
                distance[i] =
                    Vector3.Distance(m_SelfPosition, m_TargetPosition) < maxDistance
                        ? Vector3.Distance(m_SelfPosition, m_TargetPosition)
                        : maxDistance; // Calculate the distance.
                OutputMessage += distance[i] + " "; // Set the output message.
            }
        }
        //var index = distance.Count-1;
        // Get the index of the closest object.
        //Debug.Log(index);

        // Debug.Log(Index);
        string WritePath = "Data/" + "Dataset" + Index;
        string FileName = "LaserScan" + ID + ".txt";
        TextWriter.WriteToFile(WritePath, FileName, OutputMessage);

        // string DibugOutput = "Laserscan ";
        // for (int i = 0; i < DetectorsCount; i++)
        // {
        //     DibugOutput = DibugOutput + " " + distance[i];
        // }
        // Debug.Log(DibugOutput); // Show the distance.
    }
}
