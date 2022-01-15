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
            var dangerZoneCoordinates = await _dangerZoneCoordinatesRepository.GetAll(cameraId);
            if (dangerZoneCoordinates == null)
                return NotFound();

            return Ok(dangerZoneCoordinates);
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<DangerZoneCoordinates>>> GetDangerZoneCoordinates()
        {
            var dangerZoneCoordinates = await _dangerZoneCoordinatesRepository.GetAll();
            return Ok(dangerZoneCoordinates);
        }

        [HttpPost]
        public async Task<ActionResult> CreateDangerZoneCoordinates(CreateDangerZoneCoordinatesDto createDangerZoneCoordinatesDto)
        {
            var dangerZoneCoordinates = new DangerZoneCoordinates
            {
              CameraId = createDangerZoneCoordinatesDto.CameraId,
              Coordinates  = createDangerZoneCoordinatesDto.Coordinates
            };

            await _dangerZoneCoordinatesRepository.Add(dangerZoneCoordinates);
            return Ok();
        }

        [HttpDelete("{id}")]
        public async Task<ActionResult> DeleteDangerZoneCoordinates(int id)
        {
            await _dangerZoneCoordinatesRepository.Delete(id);
            return Ok();
        }

        [HttpPut("{id}")]
        public async Task<ActionResult> UpdateDangerZoneCoordinates(int id, UpdateDangerZoneCoordinatesDto updateDangerZoneCoordinatesDto)
        {
            var dangerZoneCoordinates = new DangerZoneCoordinates
            {
              Id = id,
              CameraId = updateDangerZoneCoordinatesDto.CameraId,
              Coordinates  = updateDangerZoneCoordinatesDto.Coordinates
            };

            await _dangerZoneCoordinatesRepository.Update(dangerZoneCoordinates);
            return Ok();
        }
    }
}