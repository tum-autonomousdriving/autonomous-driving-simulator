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
        static int _width = 360;
        static int _height = 160;
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
            int width = _width * 3;
            int height = _height * 1;
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

        public static void SaveTo(string dir, string file, Camera[] Cameras)
        {
            string fullPath = Path.Combine(dir, file);
            //here file name should be "xxx.png"
            int width = _width * 3;
            int height = _height * 1;

            RenderTexture combinedRenderTexture = new RenderTexture(width, height, 24);
            if (!Directory.Exists(dir))
            {
                Directory.CreateDirectory(dir);
            }
            if (!File.Exists(fullPath))
            {
                // Create a RenderTexture with the same dimensions as the camera's viewport
                for (int i = 0; i < Cameras.Length; i++)
                {
                    //create a rendertexture so that the image of camera can be rendered into it
                    RenderTexture renderTexture = new RenderTexture(_width, _height, 24);
                    //make targetTexture of camera into renderTexture
                    Cameras[i].targetTexture = renderTexture;
                    RenderTexture.active = renderTexture;
                    //trigger the render process
                    Cameras[i].Render();

                    int destX = (i % 3) * Cameras[i].pixelWidth;
                    // int destY = (i / 4) * Cameras[i].pixelHeight;
                    int destY = 0;
                    // 使用 Graphics.CopyTexture 将相机纹理的数据复制到目标纹理中的指定区域
                    Graphics.CopyTexture(
                        renderTexture,
                        0,
                        0,
                        0,
                        0,
                        _width,
                        _height,
                        combinedRenderTexture,
                        0,
                        0,
                        destX,
                        destY
                    );

                    Cameras[i].targetTexture = null;
                }
                //create a instance of texture in GPU in order to execute the operation of GPU
                combinedRenderTexture.Create();

                //read the pixels from GPU by using method AsyncGPUReadback.Request, this step reads the texture as RGB24 Format and stores it in a cache area, while also calling the callback function
                //initiates an asynGPUreadback request to retrieve the texture data.
                //可以理解为创建了一个异步读取请求，之后作为传入参数传给回调函数后用request.GetData<byte>()来得到字节串数据
                AsyncGPUReadback.Request(
                    combinedRenderTexture,
                    0,
                    TextureFormat.RGB24,
                    OnCompleteReadback
                );
                Resources.UnloadUnusedAssets();

                // Convert the texture to a byte array
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
