using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using PostureRecognitionAPI.Data;
using PostureRecognitionAPI.Models;
using System.Linq;

namespace PostureRecognitionAPI.Repositories
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

            return await (_context.DangerZoneCoordinates.Where(dzc => attribute.Contains(dzc.cameraId))).ToListAsync();
        }

        public async Task<IEnumerable<DangerZoneCoordinates>> GetAll()
        {
            return await _context.DangerZoneCoordinates.ToListAsync();
        }

        public async Task Update(DangerZoneCoordinates dangerZoneCoordinates)
        {
            var itemToUpdate = await _context.DangerZoneCoordinates.FindAsync(dangerZoneCoordinates.id);
            if (itemToUpdate == null)
                throw new NullReferenceException();

            itemToUpdate.cameraId = dangerZoneCoordinates.cameraId;
            itemToUpdate.coordinates = dangerZoneCoordinates.coordinates;
            await _context.SaveChangesAsync();
        }
    }
}