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
            // Check if there is any records retrieved with the provided id
            var postureLog = await _postureLogRepository.Get(id);
            if (postureLog == null)
                return NotFound();

            // Return the records retrieved
            return Ok(postureLog);
        }

        [HttpDelete("{id}")]
        public async Task<ActionResult> DeletePostureLog(int id)
        {
            // Call the Delete function declared in repository with a given id as input
            await _postureLogRepository.Delete(id);
            return Ok();
        }

        [HttpPut("{id}")]
        public async Task<ActionResult> UpdatePostureLog(int id, UpdatePostureLogDto updatePostureLogDto)
        {
            // Create new postureLog object with the given parameters through the DTO
            var postureLog = new PostureLog
            {
              id = id,
              cameraId = updatePostureLogDto.cameraId,
              zone = updatePostureLogDto.zone,
              postureLandmarks = updatePostureLogDto.postureLandmarks,
              classification  = updatePostureLogDto.classification,
              dateTime = DateTime.Now
            };

            // Update the specified record
            await _postureLogRepository.Update(postureLog);
            return Ok();
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<PostureLog>>> GetPostureLogs()
        {
            // Call the GetAll function declared in repository
            var postureLogs = await _postureLogRepository.GetAll();
            // Return the records retrieved
            return Ok(postureLogs);
        }

        [HttpPost]
        public async Task<ActionResult> CreatePostureLog(CreatePostureLogDto createPostureLogDto)
        {
            // Create new postureLog object with the given parameters through the DTO
            var postureLog = new PostureLog
            {
              cameraId = createPostureLogDto.cameraId,
              zone = createPostureLogDto.zone,
              postureLandmarks = createPostureLogDto.postureLandmarks,
              classification  = createPostureLogDto.classification,
              dateTime = DateTime.Now
            };

            // Add the new record
            await _postureLogRepository.Add(postureLog);
            return Ok();
        }

    }
}