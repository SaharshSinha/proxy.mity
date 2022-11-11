using System.Net.Sockets;
using System.Net;
using System.Text;

namespace TCP.Sender
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var ipEndPoint = new IPEndPoint(IPAddress.Any, 13);
            TcpListener listener = new(ipEndPoint);

            try
            {

                var message = $"📅 {DateTime.Now} 🕛";
                SendMessage(listener, message);
            }
            finally
            {
                listener.Stop();
            }
        }

        private static void SendMessage(TcpListener listener, string message)
        {
            TcpClient handler;
            NetworkStream stream;
            Console.WriteLine( $"sending {1}");
            listener.Start();
            handler = listener.AcceptTcpClientAsync().GetAwaiter().GetResult();
            Console.WriteLine( $"sending {2}");
            stream = handler.GetStream();
            var dateTimeBytes = Encoding.UTF8.GetBytes(message);
            Console.WriteLine( $"sending {3}");
            stream.WriteAsync(dateTimeBytes).GetAwaiter().GetResult();

            Console.WriteLine($"Sent message: \"{message}\"");
            Console.WriteLine( $"sending {4}");
            // Sample output:
            //     Sent message: "📅 8/22/2022 9:07:17 AM 🕛"
            //Console.WriteLine("Press enter to send another");
            //var newMessage = Console.ReadLine();
            //if (newMessage != "") SendMessage(listener, message);
        }
    }
}