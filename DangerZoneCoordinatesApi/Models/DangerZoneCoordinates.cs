using System.Linq;

namespace DangerZoneCoordinatesApi.Models
{
    public class DangerZoneCoordinates
    {
        public int Id { get; set; }
        public int CameraId { get; set; }
        public string Coordinates { get; set; }
    }
}