namespace SignalR.Hub.Pose
{
    internal class BodyAction
    {
        public static BodyAction ChillingOut => new BodyAction { IsChillingOut = true };
        public static BodyAction TurnedLeft => new BodyAction { IsTurnedLeft = true };
        public static BodyAction TurnedRight => new BodyAction { IsTurnedRight = true };

        internal bool IsChillingOut { get; private set; }
        internal bool IsTurnedLeft { get; private set; }
        internal bool IsTurnedRight { get; private set; }
        
    }
}