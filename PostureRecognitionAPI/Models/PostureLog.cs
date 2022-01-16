using System;

namespace PostureRecognitionAPI.Models
{
    public class PostureLog
    {
        public int Id { get; set; }
        public DateTime DateTime { get; set; }
        public int CameraId { get; set; }
        public string Zone { get; set; }
        public string PostureLandmarks { get; set; }
        public string Classification { get; set; }
    }
}