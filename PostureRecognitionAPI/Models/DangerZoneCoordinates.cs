using System.Linq;

namespace PostureRecognitionAPI.Models
{
    public class DangerZoneCoordinates
    {
        public int id { get; set; }
        public int cameraId { get; set; }
        public string coordinates { get; set; }
    }
}