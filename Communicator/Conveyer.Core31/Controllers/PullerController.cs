using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;

namespace SignalR.Hub.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PullerController : ControllerBase
    {
        [HttpGet]
        public IEnumerable<string> Get()
        {
            List<string> payload = new List<string>();
            while (Kyoo.Messages.TryDequeue(out var message))
            {
                payload.Add(message);
            }
            return payload;
        }

    }
}
