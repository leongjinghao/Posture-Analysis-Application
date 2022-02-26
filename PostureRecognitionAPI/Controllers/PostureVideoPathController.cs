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
    public class PostureVideoPathController : ControllerBase
    {
        private readonly IPostureVideoPathRepository _postureVideoPathRepository;
        public PostureVideoPathController(IPostureVideoPathRepository postureVideoPathRepository)
        {
            _postureVideoPathRepository = postureVideoPathRepository;

        }

        [HttpGet("{id}")]
        public async Task<ActionResult<PostureVideoPath>> GetPostureVideoPath(int id)
        {
            // Check if there is any records retrieved with the provided id
            var postureVideoPath = await _postureVideoPathRepository.Get(id);
            if (postureVideoPath == null)
                return NotFound();

            // Return the records retrieved
            return Ok(postureVideoPath);
        }

        [HttpDelete("{videoName}")]
        public async Task<ActionResult> DeletePostureVideoPath(string videoName)
        {
            // Call the Delete function declared in repository with a given id as input
            await _postureVideoPathRepository.Delete(videoName);

            return Ok();
        }

        [HttpPut("{id}")]
        public async Task<ActionResult> UpdatePostureVideoPath(int id, UpdatePostureVideoPathDto updatePostureVideoPathDto)
        {
            // Create new postureVideoPath object with the given parameters through the DTO
            var postureVideoPath = new PostureVideoPath
            {
              id = id,
              postureVideoPath = updatePostureVideoPathDto.postureVideoPath
            };

            // Update the specified record
            await _postureVideoPathRepository.Update(postureVideoPath);
            return Ok();
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<PostureVideoPath>>> GetPostureVideoPaths()
        {
            // Call the GetAll function declared in repository
            var postureVideoPaths = await _postureVideoPathRepository.GetAll();
            // Return the records retrieved
            return Ok(postureVideoPaths);
        }

        [HttpPost]
        public async Task<ActionResult> CreatePostureVideoPath(CreatePostureVideoPathDto createPostureVideoPathDto)
        {
            // Create new postureVideoPath object with the given parameters through the DTO
            var postureVideoPath = new PostureVideoPath
            {
              postureVideoPath = createPostureVideoPathDto.postureVideoPath
            };

            // Add the new record
            await _postureVideoPathRepository.Add(postureVideoPath);
            return Ok();
        }
    }
}