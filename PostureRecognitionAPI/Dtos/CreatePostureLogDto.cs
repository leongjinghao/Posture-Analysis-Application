namespace PostureRecognitionAPI.Dtos
{
    public class CreatePostureLogDto
    {
        public int CameraId { get; set; }
        public string Zone { get; set; }
        public string PostureLandmarks { get; set; }
        public string Classification { get; set; }
    }
}