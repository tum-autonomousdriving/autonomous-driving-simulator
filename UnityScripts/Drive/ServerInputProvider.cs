using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;
using System;
using NWH.Common.Input;
using TextFileEditor;
using SocketIO;
using System.Threading.Tasks;
using UnityEngine.Rendering;
using Unity.Collections;

namespace NWH.VehiclePhysics2.Input
{
    public class ServerInputProvider : VehicleInputProviderBase
    {
        public Camera[] Cameras;
        private SocketIOComponent socket_client;
        float _throttle = 0;
        float _brakes = 0;
        float _steering = 0;
        int _width = 480;
        int _height = 320;

        // *** VEHICLE BINDINGS ***
        public override float Throttle() => _throttle;

        public override float Brakes() => _brakes;

        public override float Steering() => _steering;

        // public override bool EngineStartStop() => true;

        void CaptureAndSendImage()
        {
            int width = _width * 3;
            int height = _height * 1;

            RenderTexture combinedRenderTexture = new RenderTexture(width, height, 24);

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
        }

        void OnCompleteReadback(AsyncGPUReadbackRequest request)
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

            int width = _width * 3;
            int height = _height * 1;

            //create a Texture2D object to apply the image data from the asynGPUreadback request
            Texture2D combinedTexture = new Texture2D(width, height, TextureFormat.RGB24, false);
            //put and store the original texture in combinedImage_native into Texture 2D object combinedTexture
            combinedTexture.LoadRawTextureData(combinedImage_native);
            combinedTexture.Apply();

            byte[] combinedImage = combinedTexture.EncodeToJPG(50);
            DestroyImmediate(combinedTexture);

            string base64ImageString = Convert.ToBase64String(combinedImage);
            Dictionary<string, string> data = new Dictionary<string, string>();
            data["image"] = base64ImageString;
            socket_client.Emit("send_image", new JSONObject(data));

            Debug.Log("Combined image is captured and sent successfully.");
        }

        // void OnSteer(SocketIOEvent obj)
        // {
        //     JSONObject jsonObject = obj.data;
        //     //    print(float.Parse(jsonObject.GetField("steering_angle").str));
        //     _steering = float.Parse(jsonObject.GetField("steering_angle").str);
        //     _throttle = float.Parse(jsonObject.GetField("throttle").str);
        //     _brakes = float.Parse(jsonobject.GetField("brake").str); //set the _brake to the value of the data.
        //     ServerReply(obj);
        // }

        void ServerController(SocketIOEvent obj)
        {
            JSONObject _jsonobject = obj.data;
            _throttle = float.Parse(_jsonobject.GetField("throttle").str); //set the _throtlage to the value of the data.Throttl field.
            _brakes = float.Parse(_jsonobject.GetField("brake").str); //set the _brake to the value of the data.
            _steering = float.Parse(_jsonobject.GetField("steering_angle").str); //set the _steering to the value of the data.
            ServerReply(obj);
            Debug.Log("Command recieved.");
        }

        void ServerReply(SocketIOEvent obj)
        {
            Dictionary<string, string> data = new Dictionary<string, string>();
            data["throttle"] = _throttle.ToString();
            data["brake"] = _brakes.ToString();
            data["steering_angle"] = _steering.ToString();
            // CaptureAndSendImage();
            // data["image"] = Convert.ToBase64String(combinedImage);
            socket_client.Emit("vehicle_data", new JSONObject(data));
        }

        void OnOpen(SocketIOEvent obj)
        {
            Debug.Log("Socket connection opened.");
            _throttle = 1;
            ServerReply(obj);
        }

        void OnDisconnect(SocketIOEvent obj)
        {
            Debug.Log("Socket connection closed.");
        }

        void Start()
        {
            socket_client = GameObject.Find("SocketIO").GetComponent<SocketIOComponent>();
            socket_client.On("open", OnOpen);
            socket_client.On("disconnect", OnDisconnect);
            socket_client.On("control_command", ServerController);
            // socket_client.On("control_command", OnSteer);
            InvokeRepeating("CaptureAndSendImage", 0.0f, 0.05f);
        }

        void FixedUpdate() { }
    }
}
