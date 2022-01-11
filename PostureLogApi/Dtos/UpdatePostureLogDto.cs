namespace PostureLogApi.Dtos
{
    public class UpdatePostureLogDto
    {
        public int CameraId { get; set; }
        public string Zone { get; set; }
        public string PostureLandmarks { get; set; }
        public string Classification { get; set; }
    }
}