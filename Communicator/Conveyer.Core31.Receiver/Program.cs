using System;
using System.Diagnostics;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

namespace Conveyer.Core31.Receiver
{
    class Program
    {
        static readonly HttpClient client = new HttpClient();
        static int counter = 0;
        static COMCommunicator comCommunicator = new COMCommunicator();
        private static int _multiplier = 1;
        static Stopwatch _responser = Stopwatch.StartNew();
        static string _conveyerHostName = "***REMOVED***";
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
            Console.Write("." + _responser.ElapsedMilliseconds.ToString());
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
            }
            else if (counter % 10 == 0)
                Console.Write('.');
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
                    Console.WriteLine("Retrying in 2 secs");
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
            await Task.Delay(10);
            await PollReceiver();
        }
    }
}
