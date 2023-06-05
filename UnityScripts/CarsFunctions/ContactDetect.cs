using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ContactDetect : MonoBehaviour
{
    private Rigidbody otherRigidbody;
    private float lastCollisionTime = Mathf.Infinity;
    static int Counter;

    void OnCollisionEnter(Collision collision) {
        if (collision.gameObject.GetComponent<Rigidbody>()) {
        // Do something when two Rigidbody objects make contact
        otherRigidbody = collision.gameObject.GetComponent<Rigidbody>();
        lastCollisionTime = Time.time;
        Counter++;
        string vernacontact = "Contact:"+Counter; //Used for the vernacontact message.
        Debug.Log(vernacontact);
        }
    }      

   
    void OnCollisionExit(Collision collision) {
        if (collision.gameObject.GetComponent<Rigidbody>() == otherRigidbody) {
            otherRigidbody = null;
            lastCollisionTime = Mathf.Infinity;
        }
    }

    void FixedUpdate() {
        if (otherRigidbody && otherRigidbody.velocity.magnitude < 0.1f && Time.time - lastCollisionTime > 5f) {
            // Do something when the two objects have stopped moving for more than 10 seconds
            Debug.Log("Traffic accident!");
            string Con_pos= "Position:"+transform.position; //Used for the vernacontact message.
            Debug.Log(Con_pos); //Used for the position of the objects.
            //Debug.DrawRay(gameObject.transform.position, Vector3.up, Color.red);
            //Destroy(gameObject);
            gameObject.SetActive(false); //Used for the destroy the object.
        }
    }
    // Start is called before the first frame update
    void Start()
    {
        Counter = 0;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
