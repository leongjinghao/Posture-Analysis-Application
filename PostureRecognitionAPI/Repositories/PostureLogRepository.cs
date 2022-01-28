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
        public async Task Add(PostureLog postureLog)
        {
            _context.PostureLogs.Add(postureLog);
            await _context.SaveChangesAsync();
        }

        public async Task Delete(int id)
        {
            var itemToDelete = await _context.PostureLogs.FindAsync(id);
            if (itemToDelete == null)
                throw new NullReferenceException();
            
            _context.PostureLogs.Remove(itemToDelete);
            await _context.SaveChangesAsync();
        }

        public async Task<PostureLog> Get(int id)
        {
            return await _context.PostureLogs.FindAsync(id);
        }

        public async Task<IEnumerable<PostureLog>> GetAll()
        {
            return await _context.PostureLogs.ToListAsync();
        }

        public async Task Update(PostureLog postureLog)
        {
            var itemToUpdate = await _context.PostureLogs.FindAsync(postureLog.id);
            if (itemToUpdate == null)
                throw new NullReferenceException();

            itemToUpdate.cameraId = postureLog.cameraId;
            itemToUpdate.zone = postureLog.zone;
            itemToUpdate.postureLandmarks = postureLog.postureLandmarks;
            itemToUpdate.classification = postureLog.classification;
            await _context.SaveChangesAsync();
        }
    }
}