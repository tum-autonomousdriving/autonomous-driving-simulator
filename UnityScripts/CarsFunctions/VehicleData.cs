using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TextFileEditor;
using NWH.VehiclePhysics2;
using NWH.VehiclePhysics2.Input;
using NWH.NPhysics;

public class VehicleData : MonoBehaviour
{
    Rigidbody rb;
    int Index = TextReader.ReadIntFromFile("Data/Index.txt");

    private float throttle;
    private float brakes;
    private float steering;

    VehicleController Controller;
    VehicleInputHandler inputHandler;
    // InputSystemVehicleInputProvider InputProvider;


    public Camera[] Cameras;
    private long imgIndex;

    void Awake()
    {
        rb = gameObject.GetComponentInParent(typeof(Rigidbody)) as Rigidbody;
        Controller = gameObject.GetComponent<VehicleController>();
        inputHandler = Controller.input;
        // InputProvider = gameObject.GetComponent<InputSystemVehicleInputProvider>();
        imgIndex = 0;
    }

    void Start()
    {
        InvokeRepeating("WriteData",0.5f,0.067f);
    }

    // Start is called before the first frame update

    // Update is called once per frame
    void Update() {
        
     }

    // private int ReadIndex(){
    //     int index;													//we will store the index of the file in this variable.
    //     index = Index_Reader.ReadIntFromFile(Index_fileName);
    //     index = index + 1;
    //     Index_Writer.WriteToFile(index);							//we will write the index to the file. The text writer
    //     return index-1;
    // }
    void WriteData()
    {
        ImageSaver.SaveTo(
            "Data/Dataset" + Index + "/IMG/sub" + imgIndex,
            "CapturedImage.png",
            Cameras
        );
        throttle = inputHandler.states.throttle;
        brakes = inputHandler.states.brakes;
        steering = inputHandler.states.steering;
        TextWriter.WriteToFile(
            "Data/Dataset" + Index,
            "VehicleData.txt",
                "/IMG/sub"
                + imgIndex
                + "/CapturedImage.png "
                // + "Data/Dataset"
                // + Index
                // + "/IMG/sub"
                // + imgIndex
                // + "/CapturedImage2.png "
                // + "Data/Dataset"
                // + Index
                // + "/IMG/sub"
                // + imgIndex
                // + "/CapturedImage3.png "
                + throttle
                + " "
                + brakes
                + " "
                + steering
        // + " "
        // + rb.position[0]
        // + " "
        // + rb.position[1]
        // + " "
        // + rb.position[2]
        // + " "
        // + rb.rotation[0]
        // + " "
        // + rb.rotation[1]
        // + " "
        // + rb.rotation[2]
        // + " "
        // + rb.rotation[3]
        // + " "
        // + rb.velocity[0]
        // + " "
        // + rb.velocity[1]
        // + " "
        // + rb.velocity[2]
        // + " "
        // + rb.angularVelocity[0]
        // + " "
        // + rb.angularVelocity[1]
        // + " "
        // + rb.angularVelocity[2]
        
        );
        imgIndex++; //increment image index for next image to be taken.
    }
}
