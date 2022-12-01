namespace SignalR.Hub.Pose
{
    public static class Poser
    {
        private const double ANGLE_BUFFER = 22.5;
        private const double DISTANCE_BUFFER_PERCENTAGE = 22.5;
        private const double ARM_BEND_ANGLE = 130;
        static Dictionary<BodyPoint, int> _indx = 
            new Dictionary<BodyPoint, int>
            {
                { BodyPoint.Nose, 0},
                { BodyPoint.Eye_Left, 1},
                { BodyPoint.Eye_Right, 2},
                { BodyPoint.Ear_Left, 3},
                { BodyPoint.Ear_Right, 4},
                { BodyPoint.Shoulder_Left, 5},
                { BodyPoint.Shoulder_Right, 6},
                { BodyPoint.Elbow_Left, 7},
                { BodyPoint.Elbow_Right, 8},
                { BodyPoint.Wrist_Left, 9},
                { BodyPoint.Wrist_Right, 10},
                { BodyPoint.Hip_Left, 11},
                { BodyPoint.Hip_Right, 12},
            };

        public static Move GetPose(List<(int, int)> points)
        {
            BodyAction leftHand = WhatsTheLeftHandDoing(points);
            BodyAction rightHand = WhatsTheRightHandDoing(points);
            BodyAction face = WhatsTheFaceDoing(points);

            if (leftHand.IsChillingOut)
            {
                return Move.Not;
            }
            else if (leftHand.IsTurnedLeft)
            {
                if (rightHand.IsTurnedLeft) return Move.Back;
                if (rightHand.IsTurnedRight) return Move.Forward;
                if (face.IsTurnedLeft) return Move.LookLeft;
                if (face.IsTurnedRight) return Move.LookRight;
            }
            return Move.Not;    
        }

        private static BodyAction WhatsTheFaceDoing(List<(int, int)> points)
        {
            //double distanceBetweenEyes = GetDistanceBetween(points, BodyPoint.Eye_Left, BodyPoint.Eye_Right);

            int distanceBetweenNoseAndLeftEye = GetXDistance(points, BodyPoint.Nose, BodyPoint.Eye_Left);
            int distanceBetweenNoseAndRightEye = GetXDistance(points, BodyPoint.Nose, BodyPoint.Eye_Right);
            int halfTheDistanceBetweenNoseAndLeftEye = distanceBetweenNoseAndLeftEye / 2;
            int halfTheDistanceBetweenNoseAndRightEye = distanceBetweenNoseAndRightEye / 2;
            if (distanceBetweenNoseAndLeftEye < halfTheDistanceBetweenNoseAndRightEye) return BodyAction.TurnedLeft;
            else if (distanceBetweenNoseAndRightEye < halfTheDistanceBetweenNoseAndLeftEye) return BodyAction.TurnedRight;
            else return BodyAction.ChillingOut;
        }

        private static int GetXDistance(List<(int, int)> points, BodyPoint point1, BodyPoint point2) =>
            Math.Abs(points[_indx[point1]].Item1 - points[_indx[point2]].Item1);
        
        private static double GetDistanceBetween(List<(int, int)> points, BodyPoint bodyPoint1, BodyPoint bodyPoint2) =>
            FindDistance(
                point1: points[_indx[bodyPoint1]],
                point2: points[_indx[bodyPoint2]]);

        private static double FindDistance((int, int) point1, (int, int) point2) =>
            Math.Sqrt(Math.Pow(point1.Item1 - point2.Item1, 2) + Math.Pow(point1.Item2 - point2.Item2, 2));

        private static BodyAction WhatsTheRightHandDoing(List<(int, int)> points)
        {
            var rightHandAngle = GetAngle(
                points,
                BodyPoint.Shoulder_Right,
                BodyPoint.Elbow_Right,
                BodyPoint.Wrist_Right);

            if (rightHandAngle > (ARM_BEND_ANGLE - ANGLE_BUFFER) && rightHandAngle < (ARM_BEND_ANGLE + ANGLE_BUFFER))
            {
                return BodyAction.TurnedLeft;
            }
            else if (rightHandAngle > (360 - ARM_BEND_ANGLE - ANGLE_BUFFER) && rightHandAngle < (360 - ARM_BEND_ANGLE + ANGLE_BUFFER))
            {
                return BodyAction.TurnedRight;
            }
            else
            {
                return BodyAction.ChillingOut;
            }
        }

        private static BodyAction WhatsTheLeftHandDoing(List<(int, int)> points)
        {
            var leftHandAngle = GetAngle(
                points,
                BodyPoint.Shoulder_Left,
                BodyPoint.Elbow_Left,
                BodyPoint.Wrist_Left);

            if (leftHandAngle > (ARM_BEND_ANGLE - ANGLE_BUFFER) && leftHandAngle < (ARM_BEND_ANGLE + ANGLE_BUFFER))
            {
                return BodyAction.TurnedLeft;
            }
            else
            {
                return BodyAction.ChillingOut;
            }
        }

        private static double GetAngle(
            List<(int, int)> points, 
            BodyPoint point1, 
            BodyPoint point2, 
            BodyPoint point3) =>
            FindAngle(
                p0: points[_indx[point1]],
                p1: points[_indx[point3]],
                c: points[_indx[point2]]);

        private static double FindAngle((int, int) p0, (int, int) p1, (int, int) c)
        {
            var p0c = Math.Sqrt(Math.Pow(c.Item1 - p0.Item1, 2) +
                                Math.Pow(c.Item2 - p0.Item2, 2)); // p0->c (b)   
            var p1c = Math.Sqrt(Math.Pow(c.Item1 - p1.Item1, 2) +
                                Math.Pow(c.Item2 - p1.Item2, 2)); // p1->c (a)
            var p0p1 = Math.Sqrt(Math.Pow(p1.Item1 - p0.Item1, 2) +
                                 Math.Pow(p1.Item2 - p0.Item2, 2)); // p0->p1 (c)
            var acuteAngle = (180 / Math.PI) * Math.Acos((p1c * p1c + p0c * p0c - p0p1 * p0p1) / (2 * p1c * p0c));
            if (p1.Item1 > p0.Item1)
            {
                return acuteAngle;
            }
            else
            {
                return 360 - acuteAngle;
            }
        }
    }

    
}
