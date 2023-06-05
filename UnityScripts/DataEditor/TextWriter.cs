using System.IO;
using UnityEngine;
using System.Text;
using System.Text.RegularExpressions;

namespace TextFileEditor
{
    public class TextWriter
    {
        public static void WriteToFile(string dir, string file, string content)
        {
            string fullPath = Path.Combine(dir, file);
            if (!Directory.Exists(dir))
            {
                Directory.CreateDirectory(dir);
            }
            if (!File.Exists(fullPath))
            {
                Debug.Log("File dosn't exist, create a new one.");

                using (StreamWriter sw = File.CreateText(fullPath))
                {
                    sw.Write(content + "\n");
                    //sw.Close();  //uisng会自动释放资源
                }

                Debug.Log("Create and write successfully!");
            }
            else
            {
                //单纯的写入，会清空文件原内容，再写入
                //using (StreamWriter sw = new StreamWriter(path))
                //{
                //    sw.Write(content);
                //}
                using (FileStream fs = new FileStream(fullPath, FileMode.Append))
                {
                    using (StreamWriter sw = new StreamWriter(fs))
                    {
                        sw.Write(content + "\n"); //Write在原内容基础上另取一行,WriteLine在原文最末端接上内容
                    }
                }
                // Debug.Log("Write successfully!");
            }
        }

        public static void Replace(string path, string content)
        {
            using (StreamWriter sw = new StreamWriter(path))
            {
                sw.Write(content);
                //sw.Close();  //uisng会自动释放资源
            }
        }
    }
}
