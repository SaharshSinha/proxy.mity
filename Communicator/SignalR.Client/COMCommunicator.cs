using Newtonsoft.Json;
using System.IO;

namespace SignalR.Receiver
{
    internal class COMCommunicator
    {

        private System.ComponentModel.IContainer components = null;
        private System.IO.Ports.SerialPort serialPort1;
        private bool _inited;

        public void InitializeComponent()
        {
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
                serialPort1.WriteLine(key.ToString());
                System.Console.WriteLine("sent: " + key.ToString());
            }
            catch (Exception ex)
            {
                Console.WriteLine( "Unable to send: " + ex.Message );
            }
        }

        private void serialPort1_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            string s = serialPort1.ReadExisting();//reads the serialport buffer
            System.Console.WriteLine("rcvd: " + s);
        }

    }
}