using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace SignalR.Hub.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ConveyerController : ControllerBase
    {
        [HttpGet("{message}")]
        public async Task<string> Get(string message)
        {
            Kyoo.Messages.Enqueue(message);
            //var hub = new SenderHub();
            //await hub.SendMessage("method", message);
            return "sent " + message;
            
        }
    }
}
