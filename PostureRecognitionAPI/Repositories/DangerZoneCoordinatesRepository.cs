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

        // Add new record in DangerZoneCoordinates table using a dangerZoneCoordinates object
        public async Task Add(DangerZoneCoordinates dangerZoneCoordinates)
        {
            _context.DangerZoneCoordinates.Add(dangerZoneCoordinates);
            await _context.SaveChangesAsync();
        }

        // Delete the specified record in DangerZoneCoordinates table with a given id
        public async Task Delete(int id)
        {
            // Check if the provided id exist
            var itemToDelete = await _context.DangerZoneCoordinates.FindAsync(id);
            if (itemToDelete == null)
                throw new NullReferenceException();
            
            // Delete record from table
            _context.DangerZoneCoordinates.Remove(itemToDelete);
            await _context.SaveChangesAsync();
        }

        // Get all the dangerZoneCoordinates attributes with a given cameraId
        public async Task<IEnumerable<DangerZoneCoordinates>> GetAll(int cameraId)
        {
            var attribute = new int[] { cameraId };

            // Return all the dangerZoneCoordinates retrieved in a list
            return await (_context.DangerZoneCoordinates.Where(dzc => attribute.Contains(dzc.cameraId))).ToListAsync();
        }

        // Get all the dangerZoneCoordinates attributes for all cameraId
        public async Task<IEnumerable<DangerZoneCoordinates>> GetAll()
        {
            return await _context.DangerZoneCoordinates.ToListAsync();
        }

        // Update the specified record in DangerZoneCoordinates table with a given dangerZoneCoordinates object
        public async Task Update(DangerZoneCoordinates dangerZoneCoordinates)
        {
            // Check if the id of provided dangerZoneCoordinates object exist
            var itemToUpdate = await _context.DangerZoneCoordinates.FindAsync(dangerZoneCoordinates.id);
            if (itemToUpdate == null)
                throw new NullReferenceException();

            // Update record of the id tied with the given dangerZoneCoordinates object
            itemToUpdate.cameraId = dangerZoneCoordinates.cameraId;
            itemToUpdate.coordinates = dangerZoneCoordinates.coordinates;
            await _context.SaveChangesAsync();
        }
    }
}