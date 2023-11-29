using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class JointController : MonoBehaviour
{
    [SerializeField] private Client _client;

    // Update is called once per frame
    void Update()
    {
        Debug.Log("motor0" + _client.Message["motor0"]);
        Debug.Log("motor1" + _client.Message["motor1"]);
        Debug.Log("motor2" + _client.Message["motor2"]);
        Debug.Log("motor3" + _client.Message["motor3"]);
        Debug.Log("motor4" + _client.Message["motor4"]);
    }
}
