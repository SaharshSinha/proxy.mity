namespace GCP.Receiver
{
    internal class Program
    {
        static async Task Main(string[] args)
        {
            try
            {
                var communicator = new COMCommunicator();
                communicator.InitializeComponent();
                Environment.SetEnvironmentVariable(
                    StoryConstants.APP_CRED_ENV_VARIABLE,
                    StoryConstants.PROJECT_AUTHENTICATION_JSON);
                Console.WriteLine("Hello, World!");
                await Interceptor.PullMessagesAsync(
                    projectId: "my-project-99750",
                    subscriptionId: "my-sub",
                    acknowledge: true,
                    messageHandler: c => communicator.Send(c));
            }
            catch (Exception ex)
            {
                Console.WriteLine( "There was an error");
                Console.WriteLine(  ex.Message);
            }
            
        }
    }

    internal class StoryConstants
    {
        public const string PROJECT_AUTHENTICATION_JSON = @"c:\temp\dependency-config.json";
        public const string APP_CRED_ENV_VARIABLE = "GOOGLE_APPLICATION_CREDENTIALS";
    }
}