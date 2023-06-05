using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NWH.VehiclePhysics2.Effects;
using NWH.VehiclePhysics2;
// using NWH.VehiclePhysics2.Effects.damageHandler.RepairDamage;


public class OneKeyRepair : MonoBehaviour{
    //VehicleController _vc; 			// Reference to the car's controller.
    // Start is called before the first frame update
    DamageHandler DH = new DamageHandler();
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKey (KeyCode.F2)){
			DH.Repair();
            Debug.Log("The car has been repaired.");
			}
    }
}
