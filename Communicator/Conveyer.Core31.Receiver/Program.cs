using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
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

        private const int _ABORT_TIMEOUT_MILLISECONDS = 1000;
        public const char ABORT_KEY = '5';
        long _mostRecentMessageTime;

        static async Task Main(string[] args)
        {
            _conveyerHostName = File.ReadAllText("conveyerHostName.txt");
            if (args.Length == 1)
            {
                _multiplier = int.Parse(args[0]);
            }
            comCommunicator.InitializeComponent();
            Console.WriteLine("Hello, World!");
            PollReceiver().GetAwaiter().GetResult();

        }


        private static async Task PollReceiver()
        {
            while (true)
            {
                await GetMessages();
            }
        }

        private static async Task GetMessages()
        {
            counter++;
            string responseBody = "";

            //_responser.Restart();
            responseBody = await GetHttpResponse(1);
            //Console.ForegroundColor = ConsoleColor.Magenta;
            //Console.Write("." + _responser.ElapsedMilliseconds.ToString());
            //Console.ResetColor();
            if (!string.IsNullOrEmpty(responseBody.Replace("[", "").Replace("]", "")))
            {
                Console.WriteLine();
                Console.Write("received [" + responseBody + "]");
                var directions = responseBody.Replace("\"", "").Replace("[", "").Replace("]", "").Replace(",", "");
                //Console.WriteLine($"; sending {multipliedDirections}");
                comCommunicator.Send(directions.Last());
                //comCommunicator.Send(multipliedDirections);
            }
            else if (counter % 10 == 0)
                Console.Write('.');
        }


        private static async Task<string> GetHttpResponse(int retriesLeft = 10)
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
                    return await GetHttpResponse(retriesLeft - 1);
                }
                else
                    throw;
            }

        }

    }
}
