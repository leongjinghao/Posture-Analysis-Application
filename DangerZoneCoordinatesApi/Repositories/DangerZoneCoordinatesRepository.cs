using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using DangerZoneCoordinatesApi.Data;
using DangerZoneCoordinatesApi.Models;
using System.Linq;

namespace DangerZoneCoordinatesApi.Repositories
{
    public class DangerZoneCoordinatesRepository : IDangerZoneCoordinatesRepository
    {
        private readonly IDataContext _context;
        public DangerZoneCoordinatesRepository(IDataContext context)
        {
            _context = context;

        }
        public async Task Add(DangerZoneCoordinates dangerZoneCoordinates)
        {
            _context.DangerZoneCoordinates.Add(dangerZoneCoordinates);
            await _context.SaveChangesAsync();
        }

        public async Task Delete(int id)
        {
            var itemToDelete = await _context.DangerZoneCoordinates.FindAsync(id);
            if (itemToDelete == null)
                throw new NullReferenceException();
            
            _context.DangerZoneCoordinates.Remove(itemToDelete);
            await _context.SaveChangesAsync();
        }

        public async Task<IEnumerable<DangerZoneCoordinates>> GetAll(int cameraId)
        {
            var attribute = new int[] { cameraId };

            return await (_context.DangerZoneCoordinates.Where(dzc => attribute.Contains(dzc.CameraId))).ToListAsync();
        }

        public async Task<IEnumerable<DangerZoneCoordinates>> GetAll()
        {
            return await _context.DangerZoneCoordinates.ToListAsync();
        }

        public async Task Update(DangerZoneCoordinates dangerZoneCoordinates)
        {
            var itemToUpdate = await _context.DangerZoneCoordinates.FindAsync(dangerZoneCoordinates.Id);
            if (itemToUpdate == null)
                throw new NullReferenceException();

            itemToUpdate.CameraId = dangerZoneCoordinates.CameraId;
            itemToUpdate.Coordinates = dangerZoneCoordinates.Coordinates;
            await _context.SaveChangesAsync();
        }
    }
}