using System.Collections.Concurrent;
using System.Diagnostics;
using System.Text;

namespace GCP.Sender
{
    internal class Program
    {
        private const string GCLOUD = "C:\\\\Users\\\\sahar\\\\AppData\\\\Local\\\\Google\\\\Cloud SDK\\\\google-cloud-sdk\\\\bin\\\\gcloud";

        private static HashSet<char> allowedCharacters = new HashSet<char> { '8', '4', '6', '2' };
        static ConcurrentQueue<char> _queue = new ConcurrentQueue<char>();
        static int inCome = 0;
        static int outCome = 0;

        static async Task Main(string[] args)
        {
            Environment.SetEnvironmentVariable(
                StoryConstants.APP_CRED_ENV_VARIABLE,
                StoryConstants.PROJECT_AUTHENTICATION_JSON);
            Console.WriteLine("Hello, World!");
            //Process.Start(GCLOUD, "pubsub topics create my-topic");
            //Process.Start(GCLOUD, "pubsub subscriptions create my-sub --topic my-topic");

            Task.WaitAll(
                ReadMessages(),
                CollectMessage()
            );
            //await SendMessage();
            
            //Process.Start(GCLOUD, "pubsub subscriptions delete my-sub");
            //Process.Start(GCLOUD, "pubsub topics delete my-topic");
        }

        private static async Task ReadMessages()
        {
            while (true)
            {
                int counter = 0;
                //await Task.Delay(100);
                var sb = new StringBuilder();
                while (_queue.TryDequeue(out var qued))
                {
                    outCome++;
                    //Console.WriteLine($".{qued}");
                    counter++;
                    sb.Append(qued);
                    if (counter %10 == 0)
                    {
                        string message = sb.ToString();
                        Console.WriteLine($"sending [{message}]");
                        await SendMessage(message);
                    }
                }
                if (sb.Length > 0)
                {
                    string message = sb.ToString();
                    Console.WriteLine($"sending residual [{message}]");
                    await SendMessage(message);
                }
                //sb = new StringBuilder();
                //while (_queue.TryDequeue(out var qued))
                //{
                //    outCome++;
                //    sb.Append(qued);
                //}
                //if (sb.Length > 0)
                //{
                //    string message = sb.ToString();
                //    Console.WriteLine($"sending residual [{message}]");
                //    await SendMessage(message);
                //}
                //if (_queue.Any())
                //{
                //    Console.WriteLine(  $"Tally: {inCome - outCome} : {_queue.Count}");
                //}
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
                    _queue.Enqueue(currChar);
                }
            }
        }

        private static async Task SendMessage(string message)
        {

            await Publisher.PublishMessagesAsync(
                projectId: "my-project-99750",
                topicId: "my-topic",
                messageTexts: new List<string> { message }
            );
        }
    }

    internal class StoryConstants
    {
        public const string PROJECT_AUTHENTICATION_JSON = @"c:\temp\dependency-config.json";
        public const string APP_CRED_ENV_VARIABLE = "GOOGLE_APPLICATION_CREDENTIALS";
    }

}