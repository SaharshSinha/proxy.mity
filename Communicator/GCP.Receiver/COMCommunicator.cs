using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO.Ports;

namespace GCP.Receiver
{
    internal class COMCommunicator
    {

        private System.ComponentModel.IContainer components = null;
        private SerialPort _serialPort1;
        private bool _inited;

        public void InitializeComponent()
        {
            try
            {
                Console.WriteLine("Initializing");
                if (!_inited)
                {
                    _inited = true;
                    components = new System.ComponentModel.Container();
                    _serialPort1 = new SerialPort(this.components);
                    _serialPort1.BaudRate = 115200;
                    _serialPort1.PortName = File.ReadAllText("COM.TXT");
                    _serialPort1.DataReceived += new SerialDataReceivedEventHandler(this.serialPort1_DataReceived);
                    _serialPort1.Open();
                    Console.WriteLine("Done");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error initializing COM " + ex.Message);
            }
            
        }

        public void Send(char key)
        {
            Console.WriteLine("sent: " + key.ToString());
            try
            {
                _serialPort1.WriteLine(key.ToString());
            }
            catch (Exception)
            {
                Console.WriteLine("serial IO failed failed");
            }
        }

        private void serialPort1_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            string s = _serialPort1.ReadExisting();//reads the serialport buffer
            System.Console.WriteLine("rcvd: " + s);
        }

    }
}
