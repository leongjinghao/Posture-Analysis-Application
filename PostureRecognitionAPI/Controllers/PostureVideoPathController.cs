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
            var postureVideoPath = await _postureVideoPathRepository.Get(id);
            if (postureVideoPath == null)
                return NotFound();

            return Ok(postureVideoPath);
        }

        [HttpDelete("{videoName}")]
        public async Task<ActionResult> DeletePostureVideoPath(string videoName)
        {
            await _postureVideoPathRepository.Delete(videoName);

            //TODO: delete physical video recordings located in react public folder

            return Ok();
        }

        [HttpPut("{id}")]
        public async Task<ActionResult> UpdatePostureVideoPath(int id, UpdatePostureVideoPathDto updatePostureVideoPathDto)
        {
            var postureVideoPath = new PostureVideoPath
            {
              id = id,
              postureVideoPath = updatePostureVideoPathDto.postureVideoPath
            };

            await _postureVideoPathRepository.Update(postureVideoPath);
            return Ok();
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<PostureVideoPath>>> GetPostureVideoPaths()
        {
            var postureVideoPaths = await _postureVideoPathRepository.GetAll();
            return Ok(postureVideoPaths);
        }

        [HttpPost]
        public async Task<ActionResult> CreatePostureVideoPath(CreatePostureVideoPathDto createPostureVideoPathDto)
        {
            var postureVideoPath = new PostureVideoPath
            {
              postureVideoPath = createPostureVideoPathDto.postureVideoPath
            };

            await _postureVideoPathRepository.Add(postureVideoPath);
            return Ok();
        }
    }
}