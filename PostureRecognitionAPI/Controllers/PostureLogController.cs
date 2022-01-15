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
              CameraId = createPostureLogDto.CameraId,
              Zone = createPostureLogDto.Zone,
              PostureLandmarks = createPostureLogDto.PostureLandmarks,
              Classification  = createPostureLogDto.Classification,
              DateTime = DateTime.Now
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
              Id = id,
              CameraId = updatePostureLogDto.CameraId,
              Zone = updatePostureLogDto.Zone,
              PostureLandmarks = updatePostureLogDto.PostureLandmarks,
              Classification  = updatePostureLogDto.Classification,
              DateTime = DateTime.Now
            };

            await _postureLogRepository.Update(postureLog);
            return Ok();
        }
    }
}