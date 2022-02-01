using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using PostureRecognitionAPI.Dtos;
using PostureRecognitionAPI.Models;
using PostureRecognitionAPI.Repositories;

namespace PostureRecognitionAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class VideoPathController : ControllerBase
    {
        private readonly IVideoPathRepository _videoPathRepository;
        public VideoPathController(IVideoPathRepository videoPathRepository)
        {
            _videoPathRepository = videoPathRepository;

        }

        [HttpGet("{id}")]
        public async Task<ActionResult<VideoPath>> GetVideoPath(int id)
        {
            var videoPath = await _videoPathRepository.Get(id);
            if (videoPath == null)
                return NotFound();

            return Ok(videoPath);
        }

        [HttpDelete("{videoName}")]
        public async Task<ActionResult> DeleteVideoPath(string videoName)
        {
            await _videoPathRepository.Delete(videoName);

            //TODO: delete physical video recordings located in react public folder

            return Ok();
        }

        [HttpPut("{id}")]
        public async Task<ActionResult> UpdateVideoPath(int id, UpdateVideoPathDto updateVideoPathDto)
        {
            var videoPath = new VideoPath
            {
              id = id,
              videoPath = updateVideoPathDto.videoPath
            };

            await _videoPathRepository.Update(videoPath);
            return Ok();
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<VideoPath>>> GetVideoPaths()
        {
            var videoPaths = await _videoPathRepository.GetAll();
            return Ok(videoPaths);
        }

        [HttpPost]
        public async Task<ActionResult> CreateVideoPath(CreateVideoPathDto createVideoPathDto)
        {
            var videoPath = new VideoPath
            {
              videoPath = createVideoPathDto.videoPath
            };

            await _videoPathRepository.Add(videoPath);
            return Ok();
        }
    }
}