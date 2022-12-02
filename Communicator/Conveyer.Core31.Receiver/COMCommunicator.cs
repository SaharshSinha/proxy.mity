using Newtonsoft.Json;
using System;
using System.Collections.Concurrent;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;

namespace Conveyer.Core31.Receiver
{
    internal class COMCommunicator
    {
        private System.ComponentModel.IContainer components = null;
        private System.IO.Ports.SerialPort serialPort1;
        private bool _inited;
        private char _lastSent;
        private const int _ABORT_TIMEOUT_MILLISECONDS = 1000;
        public const char ABORT_KEY = '5';
        long _mostRecentMessageTime;
        public void InitializeComponent()
        {


            if (!_inited)
            {
                _inited = true;
                openPort();
            }

            void openPort()
            {
                components = new System.ComponentModel.Container();
                serialPort1 = new System.IO.Ports.SerialPort(this.components);
                serialPort1.BaudRate = 115200;
                serialPort1.PortName = File.ReadAllText("COM.TXT");
                serialPort1.DataReceived += new System.IO.Ports.SerialDataReceivedEventHandler(this.serialPort1_DataReceived);
                serialPort1.Open();
            }
        }

        public void Send(char key)
        {
            _mostRecentMessageTime = DateTime.Now.Ticks;

            if (key.Equals(ABORT_KEY) ||
                !key.Equals(_lastSent))
            {
                Console.WriteLine();
                SendNew(key);
            }
            Task.Run(() => SendAbort(3));
        }

        private async Task SendAbort(int redundancyAttempt)
        {
            await Task.Delay(_ABORT_TIMEOUT_MILLISECONDS);
            if ((DateTime.Now.Ticks - _mostRecentMessageTime) >=
                TimeSpan.FromMilliseconds(_ABORT_TIMEOUT_MILLISECONDS).Ticks)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.Write("Cancelling - ");
                SendNew(ABORT_KEY);
                Console.ResetColor();
                if (redundancyAttempt > 0)
                {
                    await SendAbort(redundancyAttempt - 1);
                }
            }
        }

        private void SendNew(char key)
        {
            _lastSent = key;
            serialPort1.Write(key.ToString());
            Console.WriteLine("sent: " + key.ToString());
        }

        private void serialPort1_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            string s = serialPort1.ReadExisting();//reads the serialport buffer
            Console.WriteLine("; rcvd: " + s);
        }

    }
}