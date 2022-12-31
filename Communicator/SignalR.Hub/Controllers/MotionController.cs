using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using SignalR.Hub.Pose;

namespace SignalR.Hub.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MotionController : ControllerBase
    {
        private static Dictionary<Move, char> moveToCharMap = new Dictionary<Move, char>
        {
            { Move.Forward, '8' },
            { Move.Back, '2' },
            { Move.LookLeft, '4' },
            { Move.LookRight, '6' },
            { Move.Not, '5' },
        };

        [HttpGet]
        //public char Post([FromBody] List<(int, int)> payload)
        public char Get(string payload)
        {
            var points = JsonConvert.DeserializeObject<List<(int, int)>>(payload);
            Move pose = Poser.GetPose(points);

            char moveCharacter = moveToCharMap[pose];
            if (pose != Move.Not)
            {
                //Kyoo.Messages.Enqueue(moveCharacter.ToString());
            }

            return moveCharacter;
        }

        void Sample()
        {
            List<(int, int)> payload = new List<(int, int)>{(1,2),(3,4),(5,6)};
            
        }
    }
}
