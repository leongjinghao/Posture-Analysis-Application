namespace PostureRecognitionAPI.Dtos
{
    public class CreateDangerZoneCoordinatesDto
    {
        public int CameraId { get; set; }
        public string Coordinates { get; set; }
    }
}