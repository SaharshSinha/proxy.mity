using System;
using System.Collections.Generic;
using System.Collections.Specialized;

namespace SignalR.Hub
{

    public class Kyoo
    {
        private const double _MILLISECOND_RESET = 1000;
        public static Queue<string> Messages = new Queue<string>();
        private static string _latest = "UNSET";

        private static DateTime _lastSet;

        public static string Latest 
        {
            get
            {

                if ((DateTime.Now - _lastSet).TotalMilliseconds >= _MILLISECOND_RESET)
                    return "5";
                return _latest;
            }
            set
            {
                _lastSet = DateTime.Now;
                _latest = value;
            }
        }
    }
}
