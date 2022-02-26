using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using PostureRecognitionAPI.Data;
using PostureRecognitionAPI.Models;

namespace PostureRecognitionAPI.Repositories
{
    public class PostureLogRepository : IPostureLogRepository
    {
        private readonly IDataContext _context;
        public PostureLogRepository(IDataContext context)
        {
            _context = context;

        }

        // Add new record in PostureLogs table using a postureLog object
        public async Task Add(PostureLog postureLog)
        {
            _context.PostureLogs.Add(postureLog);
            await _context.SaveChangesAsync();
        }

        // Delete the specified record in PostureLogs table with a given id
        public async Task Delete(int id)
        {
            // Check if the provided id exist
            var itemToDelete = await _context.PostureLogs.FindAsync(id);
            if (itemToDelete == null)
                throw new NullReferenceException();
            
            // Delete record from table
            _context.PostureLogs.Remove(itemToDelete);
            await _context.SaveChangesAsync();
        }

        // Get the postureLog attributes with a given id
        public async Task<PostureLog> Get(int id)
        {
            return await _context.PostureLogs.FindAsync(id);
        }

        // Get all the postureLog attributes
        public async Task<IEnumerable<PostureLog>> GetAll()
        {
            return await _context.PostureLogs.ToListAsync();
        }

        // Update the specified record in PostureLogs table with a given postureLog object
        public async Task Update(PostureLog postureLog)
        {
            // Check if the id of provided postureLog object exist
            var itemToUpdate = await _context.PostureLogs.FindAsync(postureLog.id);
            if (itemToUpdate == null)
                throw new NullReferenceException();

            // Update record of the id tied with the given postureLog object
            itemToUpdate.cameraId = postureLog.cameraId;
            itemToUpdate.zone = postureLog.zone;
            itemToUpdate.postureLandmarks = postureLog.postureLandmarks;
            itemToUpdate.classification = postureLog.classification;
            await _context.SaveChangesAsync();
        }
    }
}