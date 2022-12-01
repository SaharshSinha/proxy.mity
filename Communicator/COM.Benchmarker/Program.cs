namespace COM.Benchmarker
{
    internal class Program
    {
        static COMCommunicator communicator = new COMCommunicator();
        static void Main(string[] args)
        {
            Console.WriteLine("Hello, World!");
            communicator.InitializeComponent();
            communicator.SendAsync();
            Console.WriteLine(  "Done");
            Task.WaitAll(
                PollReceiver(),
                communicator.SendAsync());
        }


        public static async Task PollReceiver()
        {
            await Task.Yield();
            while (true)
            {
                var charKey = Console.ReadKey().KeyChar;
                communicator.DirectionQueue.Enqueue(charKey.ToString());
            }
        }
    }
}