using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TextFileEditor;
using NWH.VehiclePhysics2;
using NWH.VehiclePhysics2.Input;
using NWH.NPhysics;

public class RecordControl : MonoBehaviour
{
    int Index = TextReader.ReadIntFromFile("Data/Index.txt");
    private float throttle;
    private float brakes;
    private float steering;

    VehicleController Controller;
    public VehicleInputHandler InputHandler;

    void Awake()
    {
        Controller = gameObject.GetComponent<VehicleController>();
        InputHandler = Controller.input;
    }

    void Start()
    {
    }



    // Start is called before the first frame update
    void FixedUpdate()
    {
        throttle = InputHandler.states.throttle;
        brakes = InputHandler.states.brakes;
        steering = InputHandler.states.steering;
        WriteData();
    }

    // Update is called once per frame
    void Update() { }

    // private int ReadIndex(){
    //     int index;													//we will store the index of the file in this variable.
    //     index = Index_Reader.ReadIntFromFile(Index_fileName);
    //     index = index + 1;
    //     Index_Writer.WriteToFile(index);							//we will write the index to the file. The text writer
    //     return index-1;
    // }
    void WriteData()
    {
        TextWriter.WriteToFile(
            "Data/Drive",
            "ControlData"+ Index+".txt",
                throttle
                + " "
                + brakes
                + " "
                + steering
        );
    }
}
