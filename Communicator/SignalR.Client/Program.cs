using Microsoft.AspNetCore.SignalR.Client;
using System.Diagnostics;

namespace SignalR.Receiver
{
    internal class Program
    {
        static readonly HttpClient client = new HttpClient();
        static int counter = 0;
        static COMCommunicator comCommunicator = new COMCommunicator();
        private static int _multiplier = 1;
        static Stopwatch _responser = Stopwatch.StartNew();
        static string _conveyerHostName = "***REMOVED***";
        private const int MAX_POLL_INTERVAL_SECONDS = 10;
        private const int MIN_POLL_INTERVAL_MILLISECONDS = 10;
        private static int _currentPollIntervalMilliSeconds = MIN_POLL_INTERVAL_MILLISECONDS;
        static async Task Main(string[] args)
        {
            _conveyerHostName = File.ReadAllText("conveyerHostName.txt");
            if (args.Length == 1)
            {
                _multiplier = int.Parse(args[0]);
            }
            comCommunicator.InitializeComponent(_multiplier);
            Console.WriteLine("Hello, World!");
            //await ReceiveSignalR();
            Task.WaitAll(
                PollReceiver(),
                comCommunicator.SendAsync());

        }

        private static async Task GetMessages()
        {
            counter++;
            string responseBody = "";

            _responser.Restart();
            responseBody = await GetResponse();
            Console.ForegroundColor = ConsoleColor.Magenta;
            Console.Write(_responser.ElapsedMilliseconds.ToString()+".");
            Console.ResetColor();
            // Above three lines can be replaced with new helper method below
            // string responseBody = await client.GetStringAsync(uri);
            if (!string.IsNullOrEmpty(responseBody.Replace("[", "").Replace("]", "")))
            {
                Console.WriteLine();
                Console.Write("received [" + responseBody + "]");
                var directions = responseBody.Replace("\"", "").Replace("[", "").Replace("]", "").Replace(",", "");
                var multipliedDirections =
                    string.IsNullOrEmpty(directions) ?
                    directions :
                    new string(directions[0], _multiplier);
                //Console.WriteLine($"; sending {multipliedDirections}");
                comCommunicator.DirectionQueue.Enqueue(directions);
                //comCommunicator.Send(multipliedDirections);
                _currentPollIntervalMilliSeconds = MIN_POLL_INTERVAL_MILLISECONDS;
            }
            else
            {
                _currentPollIntervalMilliSeconds *= 2;
                _currentPollIntervalMilliSeconds = Math.Min(MAX_POLL_INTERVAL_SECONDS * 1000, _currentPollIntervalMilliSeconds);
                Console.WriteLine( nameof(_currentPollIntervalMilliSeconds) + " is " + _currentPollIntervalMilliSeconds.ToString());
                if (counter % 10 == 0)
                    Console.Write('.');
            }
        }

        private static async Task<string> GetResponse(int retriesLeft = 10)
        {
            string responseBody = "";
            try
            {
                using (HttpResponseMessage response = await client.GetAsync($"{_conveyerHostName}/api/puller"))
                {
                    response.EnsureSuccessStatusCode();
                    responseBody = response.Content.ReadAsStringAsync().GetAwaiter().GetResult();
                }

                return responseBody;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"RetriesLeft: {retriesLeft}; error" + ex.Message);
                if (retriesLeft > 0)
                {
                    Console.WriteLine( "Retrying in 2 secs" );
                    await Task.Delay(2000);
                    return await GetResponse(retriesLeft - 1);
                }
                else
                    throw;
            }
         
        }

        private static async Task PollReceiver()
        {
            while (true)
            {
                await GetMessages();
                await Task.Delay(_currentPollIntervalMilliSeconds);
            }
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