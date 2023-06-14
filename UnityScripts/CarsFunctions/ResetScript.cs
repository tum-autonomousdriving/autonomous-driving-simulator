using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NWH.VehiclePhysics2;
using NWH.VehiclePhysics2.Effects;
using NWH.VehiclePhysics2.Input;

public class ResetScript : MonoBehaviour
{
    Transform myTransform;
    Rigidbody myRigibody;
    Vector3 start_pos;
	Quaternion 	start_rot;
	VehicleController Controller;
	DamageHandler damageHandler;
	InputSystemVehicleInputProvider InputProvider;


	// Use this for initialization
	void Start () {
		Controller = gameObject.GetComponent<VehicleController>();
		damageHandler = Controller.damageHandler;
		Application.targetFrameRate = 100;
		myTransform = GetComponent<Transform>();
        myRigibody = GetComponent<Rigidbody>();
        start_pos = myTransform.position;
		start_rot = myTransform.rotation;
		InputProvider = gameObject.GetComponent<InputSystemVehicleInputProvider>();
        Debug.Log(start_pos);  // prints start position
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKey (KeyCode.F1)) { 	// if the key is pressed, run the method named "Reset"){
            myRigibody.AddForce(Vector3.zero, ForceMode.Acceleration);
            myRigibody.velocity = Vector3.zero;
            myRigibody.angularVelocity = Vector3.zero;
			myTransform.SetLocalPositionAndRotation(start_pos+new Vector3(0,1,0), start_rot);
			damageHandler.Repair();
		}
		if (Input.GetMouseButtonDown(1)) { 	// if the key is pressed, run the method named "Reset"){
            InputProvider.mouseInput = !InputProvider.mouseInput;
		}
	}
}