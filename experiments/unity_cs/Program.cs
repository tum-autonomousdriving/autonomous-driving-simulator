using SocketIOClient;

var client = new SocketIO("http://localhost:5000/");

client.On("hi", response =>
{
    // You can print the returned data first to decide what to do next.
    // output: ["hi client"]
    Console.WriteLine(response);

    string text = response.GetValue<string>();

    // The socket.io server code looks like this:
    // socket.emit('hi', 'hi client');
});

client.On("test", response =>
{
    // You can print the returned data first to decide what to do next.
    // output: ["ok",{"id":1,"name":"tom"}]
    Console.WriteLine(response);
    
    // Get the first data in the response
    string text = response.GetValue<string>();
    // Get the second data in the response
    //var dto = response.GetValue<TestDTO>(1);

    // The socket.io server code looks like this:
    // socket.emit('hi', 'ok', { id: 1, name: 'tom'});
});

client.OnConnected += async (sender, e) =>
{
    // Emit a string
    await client.EmitAsync("cs_message", "你好, Python!");

    // Emit a string and an object
    //var dto = new TestDTO { Id = 123, Name = "bob" };
    //await client.EmitAsync("register", "source", dto);
};
await client.ConnectAsync();