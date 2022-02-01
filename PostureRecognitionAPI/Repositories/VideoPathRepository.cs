using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using PostureRecognitionAPI.Data;
using PostureRecognitionAPI.Models;

namespace PostureRecognitionAPI.Repositories
{
    public class VideoPathRepository : IVideoPathRepository
    {
        private readonly IDataContext _context;
        public VideoPathRepository(IDataContext context)
        {
            _context = context;

        }
        public async Task Add(VideoPath videoPath)
        {
            _context.VideoPaths.Add(videoPath);
            await _context.SaveChangesAsync();
        }

        public async Task Delete(string videoName)
        {
            var itemToDelete = await (_context.VideoPaths.Where(vp => vp.videoPath.Contains(videoName))).FirstAsync();
            if (itemToDelete == null)
                throw new NullReferenceException();
            
            _context.VideoPaths.Remove(itemToDelete);
            await _context.SaveChangesAsync();
        }

        public async Task<VideoPath> Get(int id)
        {
            return await _context.VideoPaths.FindAsync(id);
        }

        public async Task<IEnumerable<VideoPath>> GetAll()
        {
            return await _context.VideoPaths.ToListAsync();
        }

        public async Task Update(VideoPath videoPath)
        {
            var itemToUpdate = await _context.VideoPaths.FindAsync(videoPath.id);
            if (itemToUpdate == null)
                throw new NullReferenceException();

            itemToUpdate.videoPath = videoPath.videoPath;
            await _context.SaveChangesAsync();
        }
    }
}