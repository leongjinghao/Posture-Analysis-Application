namespace PostureRecognitionAPI.Dtos
{
    public class UpdateDangerZoneCoordinatesDto
    {
        public int CameraId { get; set; }
        public string Coordinates { get; set; }
    }
}