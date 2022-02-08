namespace PostureRecognitionAPI.Dtos
{
    public class CreateDangerZoneCoordinatesDto
    {
        public int cameraId { get; set; }
        public string coordinates { get; set; }
    }
}