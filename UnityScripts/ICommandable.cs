using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ICommandable : MonoBehaviour {
	
	protected TCPServer server;
    protected TimeServer time_server;

	protected string full_name;

	private static string GetGameObjectPath(Transform transform)
	{
	    string path = transform.name;
	    while (transform.parent != null)
	    {
	        transform = transform.parent;
	        path = transform.name + "/" + path;
	    }
	    return path;
	}

	public void Start() {
        time_server = (TimeServer)GameObject.FindObjectOfType(typeof(TimeServer));
	    full_name = GetGameObjectPath(transform);
		RegisterWithServer();
		OnStart();
	}

	public virtual void OnStart() {

	}

	void RegisterWithServer() {
		server = (TCPServer) GameObject.FindObjectOfType (typeof(TCPServer));
		if (server != null) {
			Debug.Log (full_name + " found TCPServer");
			server.Register (full_name, this);
		} else {
			Debug.Log (full_name + " failed to find TCPServer");
		}
	}

	public virtual bool OnCommand(string[] command) {
		return false;
	}
}

