using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;
using System;
using NWH.Common.Input;
using TextFileEditor;

namespace NWH.VehiclePhysics2.Input
{
    public class FileInputProvider : VehicleInputProviderBase
    {
        public string FilePath = "Data/TestData/Test.txt";
        public static string ControlString = "0 0 0";
        static char[] separators = { ',', ' ' };
        long Index = 0;
        float Update_Frequence = 5.0f; 

        string[] substrings = ControlString.Split(separators, StringSplitOptions.RemoveEmptyEntries);

        // *** VEHICLE BINDINGS ***
        public override float Throttle() =>
            float.Parse(substrings[0], CultureInfo.InvariantCulture.NumberFormat);

        public override float Brakes() =>
            float.Parse(substrings[1], CultureInfo.InvariantCulture.NumberFormat);

        public override float Steering() =>
            float.Parse(substrings[2], CultureInfo.InvariantCulture.NumberFormat);

        void Start()
        {
            // InvokeRepeating("FileController", 0.0f, 1/Update_Frequence);
        }

        void FileController()
        {
            string[] data = TextReader.ReadLinesFromFile(FilePath);
            ControlString = data[Index];
            substrings = ControlString.Split(separators, StringSplitOptions.RemoveEmptyEntries);
            Debug.Log(substrings[0] + " " + substrings[1] + " " + substrings[2]);

            Index++;
            if (Index==data.Length-1) Index = 0; //reset index if reached end of file.  (will wrap around to 0)
        }

        void FixedUpdate()
        {
            FileController();
        }
    }
}
