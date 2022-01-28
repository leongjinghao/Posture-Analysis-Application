using System;

namespace PostureRecognitionAPI.Models
{
    public class PostureLog
    {
        public int id { get; set; }
        public DateTime dateTime { get; set; }
        public int cameraId { get; set; }
        public string zone { get; set; }
        public string postureLandmarks { get; set; }
        public string classification { get; set; }
    }
}