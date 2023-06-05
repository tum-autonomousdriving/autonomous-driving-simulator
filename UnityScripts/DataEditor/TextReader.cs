using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;

namespace TextFileEditor
{
    public class TextReader
    {
        public static string ReadFromFile(string path)
        {
            if (!File.Exists(path))
            {
                Debug.Log("File dosn't exist!");
                return "0";
            }
            else
            {
                // string []str = File.ReadAllLines(path); //遍历一行一行读取
                // foreach (string text in str)
                // {
                //     Debug.Log(text);
                // }
                // Debug.Log("===================");
                using (StreamReader sr = new StreamReader(path, Encoding.UTF8)) //全部读取
                {
                    // sr.ReadLine(); //skip the first line.
                    string content = sr.ReadLine();
                    return content;
                }
            }
        }

        public static string[] ReadLinesFromFile(string path)
        {
            // str is a empty array that will contain all the lines read from the file.
            if (!File.Exists(path))
            {
                string []str = {"0"};
                Debug.Log("File dosn't exist!");
                return 	str;
            }
            else
            {
                string []str = File.ReadAllLines(path); //Line by line
                return 	str; //return the array of lines.
            }
        }

        public static int ReadIntFromFile(string path)
        {
            using (StreamReader reader = new StreamReader(path))
            {
                string line = reader.ReadLine(); // read the first line of the file

                if (line != null)
                {
                    int value = int.Parse(line); // parse the integer value from the line
                    return value;
                }
                else
                    return 0; // if the line is empty, return 0.
            }
        }
    }
}
