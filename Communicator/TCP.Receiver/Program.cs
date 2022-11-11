using System.Net.Sockets;
using System.Net;
using System.Text;

namespace TCP.Receiver
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var ipAddress = IPAddress.Parse("***REMOVED***");
            var ipEndPoint = new IPEndPoint(ipAddress, ***REMOVED***);

            Console.WriteLine( $"listening {1}");
            using TcpClient client = new();
            client.ConnectAsync(ipEndPoint).GetAwaiter().GetResult();
            Console.WriteLine( $"listening {2}");
            using NetworkStream stream = client.GetStream();
            var buffer = new byte[1_024];
            Console.WriteLine( $"listening {3}");
            int received = stream.ReadAsync(buffer).GetAwaiter().GetResult();

            var message = Encoding.UTF8.GetString(buffer, 0, received);
            Console.WriteLine( $"listening {4}");
            Console.WriteLine($"Message received: \"{message}\"");

            //LongMethod();
        }

        private static void LongMethod()
        {
            TcpListener server = null;
            try
            {
                // Set the TcpListener on port 13000.
                Int32 port = 13000;
                IPAddress localAddr = IPAddress.Parse("***REMOVED***");

                // TcpListener server = new TcpListener(port);
                server = new TcpListener(localAddr, port);

                // Start listening for client requests.
                server.Start();

                // Buffer for reading data
                Byte[] bytes = new Byte[256];
                String data = null;

                // Enter the listening loop.
                while (true)
                {
                    Console.Write("Waiting for a connection... ");

                    // Perform a blocking call to accept requests.
                    // You could also use server.AcceptSocket() here.
                    using TcpClient client = server.AcceptTcpClient();
                    Console.WriteLine("Connected!");

                    data = null;

                    // Get a stream object for reading and writing
                    NetworkStream stream = client.GetStream();

                    int i;

                    // Loop to receive all the data sent by the client.
                    while ((i = stream.Read(bytes, 0, bytes.Length)) != 0)
                    {
                        // Translate data bytes to a ASCII string.
                        data = System.Text.Encoding.ASCII.GetString(bytes, 0, i);
                        Console.WriteLine("Received: {0}", data);

                        // Process the data sent by the client.
                        data = data.ToUpper();

                        byte[] msg = System.Text.Encoding.ASCII.GetBytes(data);

                        // Send back a response.
                        stream.Write(msg, 0, msg.Length);
                        Console.WriteLine("Sent: {0}", data);
                    }

                    // Shutdown and end the connection
                    client.Close();
                }
            }
            catch (SocketException e)
            {
                Console.WriteLine("SocketException: {0}", e);
            }
            finally
            {
                server.Stop();
            }

            Console.WriteLine("\nHit enter to continue...");
            Console.Read();
        }
    }
}