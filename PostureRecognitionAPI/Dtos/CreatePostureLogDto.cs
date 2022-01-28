namespace PostureRecognitionAPI.Dtos
{
    public class CreatePostureLogDto
    {
        public int cameraId { get; set; }
        public string zone { get; set; }
        public string postureLandmarks { get; set; }
        public string classification { get; set; }
    }
}