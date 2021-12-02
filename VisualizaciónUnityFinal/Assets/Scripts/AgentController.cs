using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class CarData
{
    public int uniqueID;
    public Vector3 position;
}

public class AgentData{
    public List<Vector3> positions;
}

public class TrafficLightsData{
    public List<Vector3> positions;
    public List<bool> states;
}

public class ModelState{
    public string message;
    public int steps;
}

public class AgentController : MonoBehaviour
{  
    //Server paramaters
    [SerializeField] string url;
    [SerializeField] string testEP;
    [SerializeField] string initEP;
    [SerializeField] string updateEP;
    [SerializeField] string agentsEP;
    [SerializeField] string trafficLightsEP;
    [SerializeField] string trafficLightsStateEP;
    [SerializeField] string stateEP;

    //Model parameters
    [SerializeField] float updateDelay; //In seconds
    [SerializeField] GameObject carPrefab;
    [SerializeField] GameObject trafficLightsPrefab;
    [SerializeField] int numAgents;
    
    //Unity parameters
    [SerializeField] Camera MainCamera;
    Camera mainCamera;
    GameObject[] agents;
    GameObject[] trafficLights;
    List<Vector3> oldPositions;
    List<Vector3> newPositions;
     // Pause the simulation while we get the update from the server
    bool hold = true;
    bool holdTrafficLights = false;

    public float timer, dt;

    //float updateTime = 0;
    AgentData carsData; 
    TrafficLightsData trafficLightsData;
    ModelState modelSteps;

    // Start is called before the first frame update
    void Start()
    {   
        modelSteps = new ModelState();
        carsData = new AgentData();
        trafficLightsData = new TrafficLightsData();
        oldPositions = new List<Vector3>();
        newPositions = new List<Vector3>();

        agents = new GameObject[1];

        timer = updateDelay;

        for(int i = 0; i < numAgents; i++){
            agents[i] = Instantiate(carPrefab, Vector3.zero, Quaternion.identity);
        }

        StartCoroutine(TestConnection());
        StartCoroutine(SendConfiguration());
    }

    // Update is called once per frame
    void Update()
    {   
        float t = timer/updateDelay;
        // Smooth out the transition at start and end
        dt = t * t * ( 3f - 2f*t);

        // Smooth out the transition at start and end
        if (timer >= updateDelay){
            timer = 0;
            hold = true;
            holdTrafficLights = true;
            //StartCoroutine(GetModelState()); //Checks if the model is done
            StartCoroutine(UpdatePositions()); //Moves agents and trafficLights
        }

        if(!hold && !holdTrafficLights){
            //Moves agents
            for (int s = 0; s < agents.Length; s++)
            {   
                if (newPositions.Count > 0 && oldPositions.Count > 0)
                {
                    /* Vector3 interpolated = Vector3.Lerp(oldPositions[s], newPositions[s], dt);
                    agents[s].transform.localPosition = interpolated; */
                    agents[s].transform.localPosition = newPositions[s]; //Movement in "skips"
                    
                    Vector3 dir = oldPositions[s] - newPositions[s];
                    agents[s].transform.rotation = Quaternion.LookRotation(dir);
                }
            }

            timer += Time.deltaTime;
        }
    }

    IEnumerator TestConnection(){
        UnityWebRequest www = UnityWebRequest.Get(url + testEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
        }
        else{
            Debug.Log(www.error);
        }
    }

    IEnumerator GetModelState(){
        UnityWebRequest www = UnityWebRequest.Get(url + stateEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            /* isDone = JsonUtility.FromJson<ModelState>(www.downloadHandler.text);

            if (isDone.isDone == true)
            {
                Debug.Log("Model done");
            } */
        }
        else{
            Debug.Log(www.error);
        }
    }

    IEnumerator SendConfiguration(){

        WWWForm form = new WWWForm();
        //Sends the variables given in Unity, to the model
        //form.AddField("floorWidth", floorWidth.ToString());
        //form.AddField("floorHeight", floorHeight.ToString());
        form.AddField("numberAgents", numAgents.ToString());

        UnityWebRequest www = UnityWebRequest.Post(url + initEP, form);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
            StartCoroutine(GetTrafficLightsData());
            StartCoroutine(UpdateTrafficLights());
            //StartCoroutine(GetCarsData());
        }
        else{
            Debug.Log(www.error);
        }
    }

    IEnumerator UpdatePositions(){
        UnityWebRequest www = UnityWebRequest.Get(url + updateEP);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
            modelSteps = JsonUtility.FromJson<ModelState>(www.downloadHandler.text);
            if (modelSteps.steps%10 == 0){
                StartCoroutine(UpdateTrafficLights());
            }
            StartCoroutine(GetCarsData());
        }
        else{
            Debug.Log(www.error);
        }
    }

    IEnumerator GetCarsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(url + agentsEP);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            carsData = JsonUtility.FromJson<AgentData>(www.downloadHandler.text);

            // Store the old positions for each agent
            oldPositions = new List<Vector3>(newPositions);

            newPositions.Clear();

            foreach(Vector3 v in carsData.positions)
                newPositions.Add(v);

            hold = false;
        }
    }

    //Instantiates all trafficLights and asigns them inside the trafficLights array
    IEnumerator GetTrafficLightsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(url + trafficLightsEP);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            trafficLightsData = JsonUtility.FromJson<TrafficLightsData>(www.downloadHandler.text);
            trafficLights = new GameObject[trafficLightsData.positions.Count];;

            //Instantiates each traffic light and sets its initial color
            for (int i = 0; i < trafficLightsData.positions.Count; i++){
                Vector3 newPosition = trafficLightsData.positions[i];
                if (trafficLightsData.states[i] == false){ //Vertical, starts in red, "S"
                    trafficLights[i] = Instantiate(trafficLightsPrefab, newPosition, Quaternion.Euler(0, 90, 0));
                    trafficLights[i].transform.Find("Spot Light").GetComponent<Light>().color = Color.red;
                }
                else{
                    trafficLights[i] = Instantiate(trafficLightsPrefab, newPosition, Quaternion.identity);
                    trafficLights[i].transform.Find("Spot Light").GetComponent<Light>().color = Color.green;
                }
            }
        }
    }

    //Updates traffic light colors
    IEnumerator UpdateTrafficLights() 
    {
        UnityWebRequest www = UnityWebRequest.Get(url + trafficLightsEP);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            //Green: 00B001
            //Red: FF0009
            trafficLightsData = JsonUtility.FromJson<TrafficLightsData>(www.downloadHandler.text);

            //Updates the colors of the traffic lights according to the state in the mesa model
            for (int i = 0; i < trafficLightsData.states.Count; i++){
                //Debug.Log(trafficLightsData.states[i]);
                if (trafficLightsData.states[i] == false){ //Vertical, starts in red, "S"
                    trafficLights[i].transform.Find("Spot Light").GetComponent<Light>().color = Color.red;
                }
                else{
                    trafficLights[i].transform.Find("Spot Light").GetComponent<Light>().color = Color.green;
                }
            }

            holdTrafficLights = false;
        }
    }

    int isBiggest(int width, int height){
        if(width > height){
            return width;
        }
        else{
            return height;
        }
    }
}