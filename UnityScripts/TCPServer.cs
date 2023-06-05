using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.IO;
using System.Threading;
using UnityEngine;

public class TCPServer : MonoBehaviour
{
    private object syncLock = new object();

    Dictionary<string, ICommandable> commandables = new Dictionary<string, ICommandable>();

    TcpListener server;
    public string host = "localhost";
    public int port = 9998;
    private Thread tcpCommandListenerThread;
    private Thread tcpSensorListenerThread;

    private TcpClient connectedTcpClient;

    private TcpClient client;
    private Stream stream;

    private Queue<string> messageQueue = new Queue<string>();

    //TODO: split command and sensor servers into two classes
    void StartCommandThread()
    {
        tcpCommandListenerThread = new Thread(new ThreadStart(ListenForCommandConnections));
        tcpCommandListenerThread.IsBackground = true;
        tcpCommandListenerThread.Start();
    }


    void Connect()
    {
        try
        {
            client = new TcpClient();
            Debug.Log("trying to connect to " + host + " on port " + port);
            client.Connect(host, port);
            stream = client.GetStream();
        }
        catch (Exception ex)
        {
            Debug.Log(ex.Message);
        }
    }

    void Start()
    {
        QualitySettings.vSyncCount = 0;  // VSync must be disabled
        Application.targetFrameRate = 100;
        StartCommandThread();
        Connect();
    }



    public void SendHeader(uint type, string name, long ticks)
    {
        SendData(BitConverter.GetBytes(0xDEADC0DE));
        SendData(BitConverter.GetBytes(type));
        SendData(BitConverter.GetBytes(ticks));
        SendData(name);
    }

    public void SendData(Quaternion data)
    {
        SendData(BitConverter.GetBytes(data.x));
        SendData(BitConverter.GetBytes(data.y));
        SendData(BitConverter.GetBytes(data.z));
        SendData(BitConverter.GetBytes(data.w));
    }

    public void SendData(Vector3 data)
    {
        SendData(BitConverter.GetBytes(data.x));
        SendData(BitConverter.GetBytes(data.y));
        SendData(BitConverter.GetBytes(data.z));
    }

    public void SendData(string data)
    {
        SendData(Encoding.ASCII.GetBytes(data + char.MinValue));
    }

    public void SendData(float data)
    {
        SendData(BitConverter.GetBytes(data));
    }

    public void SendData(int data)
    {
        SendData(BitConverter.GetBytes(data));
    }

    public void SendData(byte[] data)
    {
        if (client.Connected)
        {
            stream.Write(data, 0, data.Length);
        }
    }

    public void Register(string client_name, ICommandable commandable)
    {
        Debug.Log("Commandable: " + client_name + " registered");
        commandables.Add(client_name, commandable);
    }

    private void ListenForCommandConnections()
    {
        try
        {
            TcpListener tcpListener = new TcpListener(IPAddress.Parse("127.0.0.1"), 9999);
            tcpListener.Start();
            Debug.Log("Command server is listening");
            Byte[] bytes = new Byte[1024];
            while (true)
            {
                using (connectedTcpClient = tcpListener.AcceptTcpClient())
                {
                    Debug.Log("Command client connected");
                    using (NetworkStream stream = connectedTcpClient.GetStream())
                    {
                        int length;
                        while ((length = stream.Read(bytes, 0, bytes.Length)) != 0)
                        {
                            byte[] incomingData = new byte[length];
                            Array.Copy(bytes, 0, incomingData, 0, length);
                            string clientMessage = Encoding.ASCII.GetString(incomingData);
                            lock (syncLock)
                            {
                                messageQueue.Enqueue(clientMessage);
                            }
                        }
                    }
                }
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("SocketException " + socketException.ToString());
        }
    }

    void ProcessMessages()
    {
        lock (syncLock)
        {
            while (messageQueue.Count > 0)
            {
                string message = messageQueue.Dequeue();
                string[] message_words = message.Split(' ');

                if (message_words.Length > 1)
                {
                    string object_name = message_words[0];
                    if (commandables.ContainsKey(object_name))
                    {
                        commandables[object_name].OnCommand(message_words);
                    }
                }

            }
        }
    }

    void FixedUpdate()
    {
        ProcessMessages();
    }

    void Update()
    {
        if (!client.Connected)
        {
            Connect();
        }
    }
}
