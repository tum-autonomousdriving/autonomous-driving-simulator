using System.IO;
using UnityEngine;
using System.Text;
using System.Text.RegularExpressions;
using Unity.Collections;
using UnityEngine.Rendering;

namespace TextFileEditor
{
    public class ImageSaver : MonoBehaviour
    {
        public static Texture2D textureToSave;
        static byte[] bytes;
        static int width = 640;
        static int height = 480;
        static void OnCompleteReadback(AsyncGPUReadbackRequest request)
        {
            if (!request.done)
            {
                Debug.Log("GPU readback request is not done yet.");
                return;
            }

            if (request.hasError)
            {
                Debug.Log("GPU readback error detected.");
                return;
            }
            //Retrieve the texture data in byte format stored in byte format from the asynGPUreadback request
            NativeArray<byte> combinedImage_native = request.GetData<byte>();
            //Debug.Log("读取到cpu所用时间: " + elapsedTime03.TotalMilliseconds + " ms");
            //create a Texture2D object to apply the image data from the asynGPUreadback request
            Texture2D combinedTexture = new Texture2D(
                width,
                height,
                TextureFormat.RGB24,
                false
            );
            //put and store the original texture in combinedImage_native into Texture 2D object combinedTexture
            combinedTexture.LoadRawTextureData(combinedImage_native);
            combinedTexture.Apply();
            //Debug.Log("将图像放到texture2d所用时间: " + elapsedTime04.TotalMilliseconds + " ms");

            bytes = combinedTexture.EncodeToPNG();
            DestroyImmediate(combinedTexture);

            // string base64ImageString = Convert.ToBase64String(combinedImage);
            // Dictionary<string, string> data = new Dictionary<string, string>();
            // data["image"] = base64ImageString;
            // socket_client.Emit("send_image", new JSONObject(data));
            // TimeSpan elapsedTime05 = DateTime.Now - startTime05;
            //Debug.Log("图像转换所用时间: " + elapsedTime05.TotalMilliseconds + " ms");
            //Debug.Log("函数OnCompleteReadback所用时间: " + elapsedTime06.TotalMilliseconds + " ms");

            //Debug.Log("Combined image is captured and sent successfully.");
        }

        public static void SaveTo(string dir, string file, Camera targetCamera)
        {
            string fullPath = Path.Combine(dir, file);
            //here file name should be "xxx.png"


            if (!Directory.Exists(dir))
            {
                Directory.CreateDirectory(dir);
            }
            if (!File.Exists(fullPath))
            {
                // Create a RenderTexture with the same dimensions as the camera's viewport
                RenderTexture renderTexture = new RenderTexture(width, height, 24);

                // Set the target texture of the camera to the RenderTexture
                targetCamera.targetTexture = renderTexture;

                // Activate the RenderTexture
                targetCamera.Render();

                // Read the pixels from the RenderTexture into the Texture2D
                RenderTexture.active = renderTexture;

                renderTexture.Create();

                // texture.ReadPixels(new Rect(0, 0, renderTexture.width, renderTexture.height), 0, 0);
                AsyncGPUReadback.Request(renderTexture, 0, TextureFormat.RGB24, OnCompleteReadback);

                // Reset the target texture of the camera
                targetCamera.targetTexture = null;

                // Release the RenderTexture resources
                RenderTexture.active = null;
                Destroy(renderTexture);

                // Convert the texture to a byte array
                // byte[] bytes = texture.EncodeToPNG();

                // Specify the file path and name
                // string filePath = Path.Combine(Application.persistentDataPath, "CapturedImage.png");

                // Write the bytes to a file
                File.WriteAllBytes(fullPath, bytes);
            }
            else
            {
                Debug.LogError("Image already exists: " + fullPath); //can be removed after testing
            }
        }
    }
}
