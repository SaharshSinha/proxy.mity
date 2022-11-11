using Microsoft.AspNetCore.SignalR.Client;

namespace SignalR.Receiver
{
    internal class Program
    {
        static readonly HttpClient client = new HttpClient();
        static int counter = 0;
        static HubConnection connection;
        static COMCommunicator comCommunicator = new COMCommunicator();
        static async Task Main(string[] args)
        {
            comCommunicator.InitializeComponent();
            Console.WriteLine("Hello, World!");
            //await ReceiveSignalR();
            await PollReceiver();

        }

        private static async Task GetMessages()
        {
            counter++;
            string responseBody = "";
            responseBody = await GetResponse();
            // Above three lines can be replaced with new helper method below
            // string responseBody = await client.GetStringAsync(uri);
            if (!string.IsNullOrEmpty(responseBody))
            {
                Console.WriteLine();
                Console.WriteLine("received [" + responseBody + "]");
                var directions = responseBody.Replace("\"", "").Replace("[", "").Replace("]", "").Replace(",", "");
                comCommunicator.Send(directions);
            }
            else if (counter % 10 == 0)
                Console.Write('.');
        }

        private static async Task<string> GetResponse(int retriesLeft = 3)
        {
            string responseBody = "";
            try
            {
                using (HttpResponseMessage response = await client.GetAsync($"http://***REMOVED***:81/api/puller"))
                {
                    response.EnsureSuccessStatusCode();
                    responseBody = response.Content.ReadAsStringAsync().GetAwaiter().GetResult();
                }

                return responseBody;
            }
            catch (Exception ex)
            {
                Console.WriteLine(  "error " + ex.Message);
                if (retriesLeft > 0)
                {
                    Console.WriteLine( "Retrying" );
                    await Task.Delay(2000);
                    return await GetResponse(retriesLeft - 1);
                }
                else
                    throw;
            }
         
        }

        private static async Task PollReceiver()
        {
            await GetMessages();
            Thread.Sleep(500);
            await PollReceiver();
        }

        //private static async Task ReceiveSignalR()
        //{
        //    connection = new HubConnectionBuilder()
        //                    //.WithUrl("http://***REMOVED***:81/ChatHub")
        //                    .WithUrl("http://localhost:44312/ChatHub")
        //                    .WithAutomaticReconnect(new[] {
        //            TimeSpan.Zero,
        //            TimeSpan.FromSeconds(2),
        //            TimeSpan.FromSeconds(5),
        //            TimeSpan.FromSeconds(10),
        //            TimeSpan.FromSeconds(10),
        //            TimeSpan.FromSeconds(10),
        //            TimeSpan.FromSeconds(10),
        //            TimeSpan.FromSeconds(10),
        //            TimeSpan.FromSeconds(10),
        //            TimeSpan.FromSeconds(10) })
        //                    .Build();

        //    Console.WriteLine("Connected");
        //    connection.Closed += async (error) =>
        //    {
        //        await Task.Delay(new Random().Next(0, 5) * 1000);
        //        await connection.StartAsync();
        //    };

        //    await BeginConnection();
        //}

        //private static async Task BeginConnection()
        //{
        //    connection.On<string, string>("ReceiveMessage", (user, message) =>
        //    {
        //        var newMessage = $"{user}: {message}";
        //        Console.WriteLine(newMessage);
                
        //    });

        //    try
        //    {
        //        await connection.StartAsync();
        //    }
        //    catch (Exception ex)
        //    {
        //        Console.WriteLine("Error " + ex.Message);

        //    }
        //}
    }
}