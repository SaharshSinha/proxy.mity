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
        public string Get() =>
            Kyoo.Latest;
    }
}
