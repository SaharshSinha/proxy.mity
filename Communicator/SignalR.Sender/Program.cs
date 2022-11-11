using Newtonsoft.Json;
using System.Collections.Concurrent;
using System.Text;

namespace SignalR.Sender
{
    internal class Program
    {
        static readonly HttpClient client = new HttpClient();

        public Program()
        {
                
        }

        static void Main(string[] args)
        {
            Console.WriteLine("Hello, World! Type away...");
            Task.WaitAll(
                CollectMessage(),
                ReadMessages());
            Console.ReadLine();
        }

        private static HashSet<char> allowedCharacters = new HashSet<char> { '8', '4', '6', '2' };
        static ConcurrentQueue<char> _queue = new ConcurrentQueue<char>();
        static int inCome = 0;
        static int outCome = 0;

        private static async  Task ReadMessages()
        {
            while (true)
            {
                int counter = 0;
                //await Task.Delay(100);
                var sb = new StringBuilder();
                while (_queue.TryDequeue(out var qued))
                {
                    outCome++;

                    counter++;
                    sb.Append(qued);
                    if (counter % 10 == 0)
                    {
                        string message = sb.ToString();
                        Console.WriteLine($"sending [{message}]");
                        SendMessage(message);
                    }
                }
                if (sb.Length > 0)
                {
                    string message = sb.ToString();
                    Console.WriteLine($"sending residual [{message}]");
                    SendMessage(message);
                }

                await Task.Delay(100);
            }
        }

        private static async Task CollectMessage()
        {
            await Task.Yield();
            char currChar = '.';
            while (currChar != '/')
            {
                currChar = Console.ReadKey().KeyChar;
                inCome++;
                if (allowedCharacters.Contains(currChar))
                {
                    Console.WriteLine("->");
                    _queue.Enqueue(currChar);
                }
            }
        }

        private static async Task SendMessage(string message)
        {
            //using HttpResponseMessage response = await client. GetAsync($"http://***REMOVED***/api/Conveyer/{message}");
            //response.EnsureSuccessStatusCode();
            //string responseBody = response.Content.ReadAsStringAsync().GetAwaiter().GetResult();
            // Above three lines can be replaced with new helper method below
            string responseBody = await client.GetStringAsync($"http://***REMOVED***/api/Conveyer/{message}");
            Console.WriteLine("sent [" + responseBody + "]");
        }
    }
}