using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using PostureLogApi.Data;
using PostureLogApi.Models;

namespace PostureLogApi.Repositories
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
            var itemToUpdate = await _context.PostureLogs.FindAsync(postureLog.Id);
            if (itemToUpdate == null)
                throw new NullReferenceException();

            itemToUpdate.CameraId = postureLog.CameraId;
            itemToUpdate.Zone = postureLog.Zone;
            itemToUpdate.PostureLandmarks = postureLog.PostureLandmarks;
            itemToUpdate.Classification = postureLog.Classification;
            await _context.SaveChangesAsync();
        }
    }
}