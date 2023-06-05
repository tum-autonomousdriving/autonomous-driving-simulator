using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class QuitScript : MonoBehaviour {

	// Use this for initialization
	void Start () {
		Application.targetFrameRate = 100;
		
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKey ("escape")){
			Application.Quit();
			//System.Diagnostics.Process.GetCurrentProcess ().Kill();
				}
		
	}
}
