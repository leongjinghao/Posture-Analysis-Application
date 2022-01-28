using System;
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
    public class PostureLogController : ControllerBase
    {
        private readonly IPostureLogRepository _postureLogRepository;
        public PostureLogController(IPostureLogRepository postureLogRepository)
        {
            _postureLogRepository = postureLogRepository;

        }

        [HttpGet("{id}")]
        public async Task<ActionResult<PostureLog>> GetPostureLog(int id)
        {
            var postureLog = await _postureLogRepository.Get(id);
            if (postureLog == null)
                return NotFound();

            return Ok(postureLog);
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<PostureLog>>> GetPostureLogs()
        {
            var postureLogs = await _postureLogRepository.GetAll();
            return Ok(postureLogs);
        }

        [HttpPost]
        public async Task<ActionResult> CreatePostureLog(CreatePostureLogDto createPostureLogDto)
        {
            var postureLog = new PostureLog
            {
              cameraId = createPostureLogDto.cameraId,
              zone = createPostureLogDto.zone,
              postureLandmarks = createPostureLogDto.postureLandmarks,
              classification  = createPostureLogDto.classification,
              dateTime = DateTime.Now
            };

            await _postureLogRepository.Add(postureLog);
            return Ok();
        }

        [HttpDelete("{id}")]
        public async Task<ActionResult> DeletePostureLog(int id)
        {
            await _postureLogRepository.Delete(id);
            return Ok();
        }

        [HttpPut("{id}")]
        public async Task<ActionResult> UpdatePostureLog(int id, UpdatePostureLogDto updatePostureLogDto)
        {
            var postureLog = new PostureLog
            {
              id = id,
              cameraId = updatePostureLogDto.cameraId,
              zone = updatePostureLogDto.zone,
              postureLandmarks = updatePostureLogDto.postureLandmarks,
              classification  = updatePostureLogDto.classification,
              dateTime = DateTime.Now
            };

            await _postureLogRepository.Update(postureLog);
            return Ok();
        }
    }
}