//Client

using UnityEngine;
using System.Collections;
using System.Net.Sockets;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;

public class Client : MonoBehaviour
{
    private ClientThread ct;

    private bool isReceive;
    public Dictionary<string, int> Message;

    private void Start()
    {
        ct = new ClientThread(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp, "10.100.3.18", 8000);
        ct.StartConnect();
    }

    void Update()
    {
        // ClientJsn = new ClientJson();

        ct.Receive();

        if (ct.receiveMessage != null)
        {
            
            Dictionary<string, int> motor_position = JsonConvert.DeserializeObject<Dictionary<string, int>>(ct.receiveMessage);
            Message = motor_position;
            // Debug.Log("Server:" + Message["motor0"]);
        }
        // Msg: 

        // Clear Msg
        ct.receiveMessage = null;
    }
    
    private void OnApplicationQuit()
    {
        ct.StopConnect();
    }
}