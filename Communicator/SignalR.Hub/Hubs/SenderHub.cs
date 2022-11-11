namespace SignalR.Hub.Hubs
{
    using Microsoft.AspNetCore.SignalR;

    public class SenderHub : Hub
    {
        public async Task SendMessage(string user, string message)
        {
            await Clients.All.SendAsync("ReceiveMessage", user, message);
        }
    }
    
}
