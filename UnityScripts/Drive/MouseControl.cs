using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NWH.VehiclePhysics2;
using NWH.VehiclePhysics2.Input;

public class MouseControl : MonoBehaviour
{

	VehicleController Controller;
	InputSystemVehicleInputProvider InputProvider;


	// Use this for initialization
	void Start () {
		Controller = gameObject.GetComponent<VehicleController>();

	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetMouseButtonDown(2)) { 	// if the key is pressed, run the method named "Reset"){
            InputProvider.mouseInput = !InputProvider.mouseInput;
            Debug.Log("MouseControl");
		}
	}
}