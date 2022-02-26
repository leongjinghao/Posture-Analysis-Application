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
    public class DangerZoneCoordinatesController : ControllerBase
    {
        private readonly IDangerZoneCoordinatesRepository _dangerZoneCoordinatesRepository;
        public DangerZoneCoordinatesController(IDangerZoneCoordinatesRepository dangerZoneCoordinatesRepository)
        {
            _dangerZoneCoordinatesRepository = dangerZoneCoordinatesRepository;

        }

        [HttpGet("{cameraId}")]
        public async Task<ActionResult<DangerZoneCoordinates>> GetDangerZoneCoordinates(int cameraId)
        {
            // Check if there is any records retrieved with the provided cameraId
            var dangerZoneCoordinates = await _dangerZoneCoordinatesRepository.GetAll(cameraId);
            if (dangerZoneCoordinates == null)
                return NotFound();

            // Return the records retrieved
            return Ok(dangerZoneCoordinates);
        }
        
        [HttpDelete("{id}")]
        public async Task<ActionResult> DeleteDangerZoneCoordinates(int id)
        {
            // Call the Delete function declared in repository with a given id as input
            await _dangerZoneCoordinatesRepository.Delete(id);
            return Ok();
        }

        [HttpPut("{id}")]
        public async Task<ActionResult> UpdateDangerZoneCoordinates(int id, UpdateDangerZoneCoordinatesDto updateDangerZoneCoordinatesDto)
        {
            // Create new dangerZoneCoordinates object with the given parameters through the DTO
            var dangerZoneCoordinates = new DangerZoneCoordinates
            {
              id = id,
              cameraId = updateDangerZoneCoordinatesDto.cameraId,
              coordinates  = updateDangerZoneCoordinatesDto.coordinates
            };

            // Update the specified record
            await _dangerZoneCoordinatesRepository.Update(dangerZoneCoordinates);
            return Ok();
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<DangerZoneCoordinates>>> GetDangerZoneCoordinates()
        {
            // Call the GetAll function declared in repository
            var dangerZoneCoordinates = await _dangerZoneCoordinatesRepository.GetAll();
            // Return the records retrieved
            return Ok(dangerZoneCoordinates);
        }

        [HttpPost]
        public async Task<ActionResult> CreateDangerZoneCoordinates(CreateDangerZoneCoordinatesDto createDangerZoneCoordinatesDto)
        {
            // Create new dangerZoneCoordinates object with the given parameters through the DTO
            var dangerZoneCoordinates = new DangerZoneCoordinates
            {
              cameraId = createDangerZoneCoordinatesDto.cameraId,
              coordinates  = createDangerZoneCoordinatesDto.coordinates
            };

            // Add the new record
            await _dangerZoneCoordinatesRepository.Add(dangerZoneCoordinates);
            return Ok();
        }
    }
}