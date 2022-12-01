using Newtonsoft.Json;
using System.Collections.Concurrent;
using System.Diagnostics;
using System.IO;

namespace SignalR.Receiver
{
    internal class COMCommunicator
    {

        private System.ComponentModel.IContainer components = null;
        private System.IO.Ports.SerialPort serialPort1;
        private bool _inited;
        public ConcurrentQueue<string> DirectionQueue = new ConcurrentQueue<string>();
        Stopwatch sw = new Stopwatch();
        private int _multiplier = 1;
        int messagCounter = 0;
        Stopwatch mqTime = new Stopwatch();
        public void InitializeComponent(int multiplier)
        {
            _multiplier = multiplier;
            if (!_inited)
            {
                try
                {
                    _inited = true;
                    components = new System.ComponentModel.Container();
                    serialPort1 = new System.IO.Ports.SerialPort(this.components);
                    serialPort1.BaudRate = 115200;
                    serialPort1.PortName = File.ReadAllText("COM.TXT");
                    serialPort1.DataReceived += new System.IO.Ports.SerialDataReceivedEventHandler(this.serialPort1_DataReceived);
                    serialPort1.Open();
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Error initializing com");
                    Console.WriteLine(JsonConvert.SerializeObject(ex, Formatting.Indented));
                }
            }
        }

        public async Task SendAsync()
        {
            await Task.Yield();

            while (true)
            {
                if (DirectionQueue.TryDequeue(out string? direction))
                {
                    Console.WriteLine("dequeued " + direction + " remaining " + string.Join(",", DirectionQueue));
                    Send(direction);
                }
            }
        }

        public void Send(string keys)
        {
            foreach (var key in keys)
            {
                Send(key);
            }
        }

        public void Send(char key)
        {
            try
            {

                if (messagCounter % 10 == 0)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("Sent 10 messages in " + mqTime.ElapsedMilliseconds + " ms");
                    mqTime.Restart();
                    Console.ResetColor();
                }
                sw.Reset();
                sw.Start();
                string textToSend = key.ToString();
                serialPort1.Write(textToSend);
                Console.ForegroundColor = ConsoleColor.Green;
                Console.Write("sent: " + key.ToString() + " in " + sw.Elapsed.TotalMilliseconds.ToString() + " ms;");
                Console.ResetColor();
                //for (int i = 0; i < _multiplier - 1; i++)
                //{
                //    Thread.Sleep(1);
                //    serialPort1.Write(textToSend);
                //}
                messagCounter++;

            }
            catch (Exception ex)
            {
                Console.WriteLine( "Unable to send: " + ex.Message );
            }
        }

        private void serialPort1_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            string s = serialPort1.ReadExisting();//reads the serialport buffer
            Console.ForegroundColor = ConsoleColor.Blue;
            Console.WriteLine(" rcvd: " + s + " after " + sw.Elapsed.TotalMilliseconds.ToString() + " ms");
            Console.ResetColor();
        }

    }
}