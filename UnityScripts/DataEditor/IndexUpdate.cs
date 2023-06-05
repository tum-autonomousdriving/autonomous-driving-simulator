using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TextFileEditor;

public class IndexUpdate : MonoBehaviour
{
    //IMPORTANT: this component must be before other TextFileEditor Components!

    // Start is called before the first frame update
    void Start()
    {
        int Index;
        Index = TextReader.ReadIntFromFile("Data/Index.txt");
        TextWriter.Replace("Data/Index.txt", (Index + 1).ToString());
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
