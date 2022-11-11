using Google.Cloud.PubSub.V1;
using System;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

public class Interceptor
{
    private static HashSet<char> allowedCharacters = new HashSet<char> { '8', '4', '6', '2' };
    public static async Task<int> PullMessagesAsync(
        string projectId, 
        string subscriptionId, 
        bool acknowledge,
        Action<char> messageHandler)
    {
        //SubscriptionName subscriptionName = SubscriptionName.Parse(subscriptionNm); 
        SubscriptionName subscriptionName = SubscriptionName.FromProjectSubscription(projectId, subscriptionId);
        Console.WriteLine( "Got sub name " + subscriptionName.ToString());
        SubscriberClient subscriber = await SubscriberClient.CreateAsync(subscriptionName);
        // SubscriberClient runs your message handle function on multiple
        // threads to maximize throughput.
        int messageCount = 0;
        Task startTask = subscriber.StartAsync(
            (PubsubMessage message, CancellationToken cancel) =>
        {
            try
            {
                string text = System.Text.Encoding.UTF8.GetString(message.Data.ToArray());
                Console.WriteLine($"Message {message.MessageId}: {text}");
                Interlocked.Increment(ref messageCount);
                foreach (var charInstruction in text.Where(c => allowedCharacters.Contains(c)))
                {
                    messageHandler.Invoke(charInstruction);
                }
                return Task.FromResult(acknowledge ?
                    SubscriberClient.Reply.Ack :
                    SubscriberClient.Reply.Nack);
            }
            catch (Exception ex)
            {
                Console.WriteLine( "Error while getting sub - " + ex.Message );
                return null;
            }
            
        });
        // Run for 5 seconds.
        Console.WriteLine( "started reading, press enter to exit");
        Console.ReadLine();
        await Task.Delay(50000);
        await subscriber.StopAsync(CancellationToken.None);
        // Lets make sure that the start task finished successfully after the call to stop.
        await startTask;
        return messageCount;
    }

}